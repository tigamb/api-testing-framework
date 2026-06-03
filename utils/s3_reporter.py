# utils/s3_reporter.py

import boto3
import os
from botocore.config import Config
from datetime import datetime
from config.logger import logger
from config.settings import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_BUCKET_NAME,
    AWS_REGION
)


def upload_report_to_s3(report_path: str):
    if not all([AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_BUCKET_NAME]):
        logger.warning("פרטי AWS חסרים ב־.env — דוח לא הועלה ל־S3")
        return None

    if not os.path.exists(report_path):
        logger.error(f"קובץ הדוח לא נמצא: {report_path}")
        return None

    try:
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION,
            config=Config(signature_version="s3v4")
        )

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.basename(report_path)
        s3_key = f"reports/{timestamp}/{filename}"

        s3_client.upload_file(
            report_path,
            AWS_BUCKET_NAME,
            s3_key,
            ExtraArgs={"ContentType": "text/html"}
        )

        presigned_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": AWS_BUCKET_NAME, "Key": s3_key},
            ExpiresIn=3600
        )

        logger.info(f"דוח הועלה בהצלחה ל־S3")
        logger.info(f"קישור זמני (תקף שעה): {presigned_url}")
        return presigned_url

    except Exception as e:
        logger.error(f"שגיאה בהעלאה ל־S3: {e}")
        return None