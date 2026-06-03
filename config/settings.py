
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")
REQRES_URL = os.getenv("REQRES_URL", "https://reqres.in/api")
TIMEOUT = int(os.getenv("TIMEOUT", "10"))

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Performance thresholds (seconds)
PERF_MAX_RESPONSE_TIME = float(os.getenv("PERF_MAX_RESPONSE_TIME", "2.0"))
PERF_ACCEPTABLE_RESPONSE_TIME = float(os.getenv("PERF_ACCEPTABLE_RESPONSE_TIME", "1.0"))
PERF_MAX_STD_DEV = float(os.getenv("PERF_MAX_STD_DEV", "0.5"))

SEND_EMAIL_REPORT = os.getenv("SEND_EMAIL_REPORT", "false").lower() == "true"


# AWS
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# CloudWatch — מדדי בדיקות (שלב 30)
SEND_CLOUDWATCH_METRICS = os.getenv("SEND_CLOUDWATCH_METRICS", "false").lower() == "true"
CLOUDWATCH_NAMESPACE = os.getenv("CLOUDWATCH_NAMESPACE", "API-Testing")

# EC2 — הרצת בדיקות בענן (שלב 29)
# AMI ברירת מחדל: Amazon Linux 2023, us-east-1 (החלף לפי region שלך)
EC2_AMI_ID = os.getenv("EC2_AMI_ID", "ami-0c02fb55956c7d316")
EC2_INSTANCE_TYPE = os.getenv("EC2_INSTANCE_TYPE", "t2.micro")
EC2_IAM_INSTANCE_PROFILE = os.getenv("EC2_IAM_INSTANCE_PROFILE")  # שם ה-IAM Role — חובה
EC2_KEY_NAME = os.getenv("EC2_KEY_NAME")           # אופציונלי: גישת SSH לדיבאג
EC2_SUBNET_ID = os.getenv("EC2_SUBNET_ID")         # אופציונלי: subnet ספציפי
EC2_SECURITY_GROUP_ID = os.getenv("EC2_SECURITY_GROUP_ID")  # אופציונלי