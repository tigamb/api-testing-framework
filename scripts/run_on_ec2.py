"""
Step 29 – הרצת בדיקות על EC2

מה הסקריפט עושה:
  1. אורז את קוד הפרויקט ל-ZIP ומעלה ל-S3
  2. מעלה את קובץ .env ל-S3 (לשימוש ה-instance בלבד)
  3. מפעיל EC2 instance עם user-data שמריץ את הבדיקות
  4. ממתין עד שה-instance מסיים ומעלה done-marker ל-S3
  5. מדפיס את כתובת הדוח ב-S3

דרישות מוקדמות:
  - IAM Instance Profile עם הרשאות S3 (ולאופציונלי SSM)
  - משתני סביבה (ראה .env.example תחת # EC2)

הרצה:
  python scripts/run_on_ec2.py
"""

import base64
import json
import os
import sys
import tempfile
import time
import zipfile
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import boto3

from config.logger import logger
from config.settings import (
    AWS_ACCESS_KEY_ID,
    AWS_BUCKET_NAME,
    AWS_REGION,
    AWS_SECRET_ACCESS_KEY,
    EC2_AMI_ID,
    EC2_IAM_INSTANCE_PROFILE,
    EC2_INSTANCE_TYPE,
    EC2_KEY_NAME,
    EC2_SECURITY_GROUP_ID,
    EC2_SUBNET_ID,
)

PROJECT_ROOT = Path(__file__).parent.parent

_SKIP_DIRS = {"venv", ".git", "__pycache__", "allure-results", "logs", ".pytest_cache", "scripts"}
_SKIP_FILES = {"report.html"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _create_zip(dest: str) -> None:
    """Pack the project (excluding venv, git, etc.) into a ZIP file."""
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as zf:
        for item in PROJECT_ROOT.rglob("*"):
            parts = item.relative_to(PROJECT_ROOT).parts
            if any(p in _SKIP_DIRS for p in parts):
                continue
            if item.is_file() and item.name not in _SKIP_FILES:
                zf.write(item, item.relative_to(PROJECT_ROOT))


def _upload(s3, local: str, key: str) -> None:
    s3.upload_file(local, AWS_BUCKET_NAME, key)


def _build_user_data(zip_key: str, env_key: str, run_id: str) -> str:
    """Return base64-encoded bash script for EC2 user-data."""
    script = f"""#!/bin/bash
set -e
exec > /var/log/api-test-runner.log 2>&1

echo "=== EC2 API Test Runner – run_id: {run_id} ==="
date

# Package manager update + minimal deps (AWS CLI is pre-installed on AL2023)
yum install -y python3-pip unzip 2>/dev/null || apt-get install -y python3-pip unzip 2>/dev/null || true

# ---- Download project ----
aws s3 cp s3://{AWS_BUCKET_NAME}/{zip_key} /tmp/project.zip --region {AWS_REGION}
unzip -q /tmp/project.zip -d /tmp/project

# ---- Download .env (optional) ----
aws s3 cp s3://{AWS_BUCKET_NAME}/{env_key} /tmp/project/.env --region {AWS_REGION} 2>/dev/null || echo ".env not found, continuing without it"

cd /tmp/project

# ---- Install Python dependencies ----
pip3 install -q -r requirements.txt

# ---- Run tests (failure allowed so report is always uploaded) ----
echo "=== Running pytest ==="
python3 -m pytest tests/ -v --html=report.html --self-contained-html
TEST_EXIT=$?
echo "pytest exit code: $TEST_EXIT"

# ---- Upload HTML report to S3 ----
aws s3 cp report.html \
    s3://{AWS_BUCKET_NAME}/reports/{run_id}/report.html \
    --content-type "text/html" \
    --region {AWS_REGION} || true

# ---- Write completion marker ----
echo '{{"exit_code": '"$TEST_EXIT"', "run_id": "{run_id}"}}' > /tmp/done.json
aws s3 cp /tmp/done.json \
    s3://{AWS_BUCKET_NAME}/ec2-runs/{run_id}/done.json \
    --region {AWS_REGION}

echo "=== Done ==="
date

# ---- Self-terminate ----
INSTANCE_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
aws ec2 terminate-instances --instance-ids "$INSTANCE_ID" --region {AWS_REGION}
"""
    return base64.b64encode(script.encode()).decode()


def _wait_for_done(s3, run_id: str, timeout: int = 900, interval: int = 20) -> dict | None:
    """Poll S3 for the done marker. Returns parsed JSON or None on timeout."""
    key = f"ec2-runs/{run_id}/done.json"
    deadline = time.monotonic() + timeout
    attempt = 0

    while time.monotonic() < deadline:
        attempt += 1
        try:
            obj = s3.get_object(Bucket=AWS_BUCKET_NAME, Key=key)
            return json.loads(obj["Body"].read())
        except s3.exceptions.NoSuchKey:
            remaining = int(deadline - time.monotonic())
            logger.info(f"ממתין לסיום EC2… (ניסיון {attempt}, נותרו ~{remaining}s)")
            time.sleep(interval)
        except Exception as exc:
            logger.warning(f"שגיאה בבדיקת marker: {exc}")
            time.sleep(interval)

    return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_tests_on_ec2() -> None:
    missing = [v for v in [AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_BUCKET_NAME, EC2_IAM_INSTANCE_PROFILE] if not v]
    if missing:
        logger.error(
            "חסרים משתני .env נדרשים. ודא ש-AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, "
            "AWS_BUCKET_NAME ו-EC2_IAM_INSTANCE_PROFILE מוגדרים."
        )
        sys.exit(1)

    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    logger.info(f"מתחיל הרצת בדיקות על EC2 — run_id: {run_id}")

    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
    )
    s3 = session.client("s3")
    ec2 = session.client("ec2")

    # 1. Package project → upload to S3
    with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp:
        zip_path = tmp.name

    try:
        logger.info("אורז את הפרויקט…")
        _create_zip(zip_path)
        zip_key = f"ec2-runs/{run_id}/project.zip"
        logger.info(f"מעלה ZIP ל-S3: {zip_key}")
        _upload(s3, zip_path, zip_key)
    finally:
        os.unlink(zip_path)

    # 2. Upload .env (if exists)
    env_key = f"ec2-runs/{run_id}/.env"
    env_path = PROJECT_ROOT / ".env"
    if env_path.exists():
        logger.info("מעלה .env ל-S3 (גישה פרטית)…")
        _upload(s3, str(env_path), env_key)
    else:
        logger.warning("קובץ .env לא נמצא — ממשיך ללא הגדרות נוספות")

    # 3. Launch EC2 instance
    user_data = _build_user_data(zip_key, env_key, run_id)

    launch_params: dict = {
        "ImageId": EC2_AMI_ID,
        "InstanceType": EC2_INSTANCE_TYPE,
        "MinCount": 1,
        "MaxCount": 1,
        "UserData": user_data,
        "IamInstanceProfile": {"Name": EC2_IAM_INSTANCE_PROFILE},
        "TagSpecifications": [{
            "ResourceType": "instance",
            "Tags": [
                {"Key": "Name", "Value": f"api-test-runner-{run_id}"},
                {"Key": "Project", "Value": "api-testing-framework"},
            ],
        }],
    }

    if EC2_KEY_NAME:
        launch_params["KeyName"] = EC2_KEY_NAME
    if EC2_SUBNET_ID:
        launch_params["SubnetId"] = EC2_SUBNET_ID
    if EC2_SECURITY_GROUP_ID:
        launch_params["SecurityGroupIds"] = [EC2_SECURITY_GROUP_ID]

    logger.info(f"מפעיל EC2 instance ({EC2_INSTANCE_TYPE}, AMI: {EC2_AMI_ID})…")
    resp = ec2.run_instances(**launch_params)
    instance_id = resp["Instances"][0]["InstanceId"]
    logger.info(f"Instance הופעל: {instance_id}")
    logger.info(f"לוגים ב-instance: /var/log/api-test-runner.log")

    # 4. Wait for completion marker
    result = _wait_for_done(s3, run_id)

    if result is None:
        logger.error(f"תם הזמן — הבדיקות לא הסתיימו בזמן המוגדר (15 דקות)")
        logger.info(f"בדוק את ה-instance ידנית: {instance_id} | region: {AWS_REGION}")
        sys.exit(1)

    exit_code = result.get("exit_code", -1)
    report_url = (
        f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/"
        f"reports/{run_id}/report.html"
    )

    if exit_code == 0:
        logger.info("הבדיקות עברו בהצלחה!")
    else:
        logger.warning(f"חלק מהבדיקות נכשלו (exit code: {exit_code})")

    logger.info(f"דוח HTML ב-S3: {report_url}")


if __name__ == "__main__":
    run_tests_on_ec2()
