
import yagmail
import os
from datetime import datetime
from config.logger import logger


def send_test_report(report_path: str, s3_url: str = None):
    sender_email = os.getenv("EMAIL_SENDER")
    receiver_email = os.getenv("EMAIL_RECEIVER")
    email_password = os.getenv("EMAIL_PASSWORD")

    if not all([sender_email, receiver_email, email_password]):
        logger.warning("פרטי מייל חסרים ב־.env — דוח לא נשלח")
        return

    subject = f"דוח בדיקות API – {datetime.now().strftime('%d/%m/%Y %H:%M')}"

    s3_line = f"\nקישור לדוח ב־S3:\n{s3_url}" if s3_url else ""

    body = f"""
    שלום,

    מצורף דוח הבדיקות האוטומטיות האחרון.
    {s3_line}

    בברכה,
    API Testing Framework
    """

    try:
        yag = yagmail.SMTP(sender_email, email_password)
        yag.send(
            to=receiver_email,
            subject=subject,
            contents=body,
            attachments=report_path
        )
        logger.info(f"דוח נשלח בהצלחה ל־{receiver_email}")

    except Exception as e:
        logger.error(f"שגיאה בשליחת הדוח: {e}")