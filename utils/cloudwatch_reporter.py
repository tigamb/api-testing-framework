# utils/cloudwatch_reporter.py

import os
import boto3
from datetime import datetime, timezone
from config.logger import logger
from config.settings import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION,
    SEND_CLOUDWATCH_METRICS,
    CLOUDWATCH_NAMESPACE,
)


def send_test_metrics(passed: int, failed: int, errors: int, duration: float) -> None:
    """
    שולח מדדי ריצת בדיקות כ-custom metrics ל-CloudWatch.

    מדדים:
      TestsPassed, TestsFailed, TestsErrors, TestsTotal, TestsDuration
    """
    if not SEND_CLOUDWATCH_METRICS:
        return

    if not all([AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, CLOUDWATCH_NAMESPACE]):
        logger.warning("פרטי CloudWatch חסרים ב-.env — מדדים לא נשלחו")
        return

    environment = os.getenv("ENVIRONMENT", "local")
    now = datetime.now(timezone.utc)
    total = passed + failed + errors

    dimensions = [
        {"Name": "Environment", "Value": environment},
        {"Name": "Project",     "Value": "api-testing-framework"},
    ]

    metric_data = [
        {
            "MetricName": "TestsPassed",
            "Dimensions": dimensions,
            "Timestamp": now,
            "Value": passed,
            "Unit": "Count",
        },
        {
            "MetricName": "TestsFailed",
            "Dimensions": dimensions,
            "Timestamp": now,
            "Value": failed,
            "Unit": "Count",
        },
        {
            "MetricName": "TestsErrors",
            "Dimensions": dimensions,
            "Timestamp": now,
            "Value": errors,
            "Unit": "Count",
        },
        {
            "MetricName": "TestsTotal",
            "Dimensions": dimensions,
            "Timestamp": now,
            "Value": total,
            "Unit": "Count",
        },
        {
            "MetricName": "TestsDuration",
            "Dimensions": dimensions,
            "Timestamp": now,
            "Value": round(duration, 2),
            "Unit": "Seconds",
        },
    ]

    try:
        cw = boto3.client(
            "cloudwatch",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION,
        )
        cw.put_metric_data(Namespace=CLOUDWATCH_NAMESPACE, MetricData=metric_data)
        logger.info(
            f"CloudWatch metrics נשלחו — namespace: {CLOUDWATCH_NAMESPACE} | "
            f"passed={passed}, failed={failed}, errors={errors}, duration={duration:.1f}s"
        )

    except Exception as e:
        logger.error(f"שגיאה בשליחת metrics ל-CloudWatch: {e}")
