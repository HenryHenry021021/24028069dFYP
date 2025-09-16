import os
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_HOST = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("EMAIL_USER")
SMTP_PASS = os.getenv("EMAIL_PASS")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USER)
SMTP_FROM_NAME = os.getenv("SMTP_FROM_NAME", "FastAPI Service")


def generate_code() -> str:
    """生成 6 位数字验证码"""
    return str(random.randint(0, 999999)).zfill(6)


def send_captcha_email(recipient: str, code: str) -> None:
    """发送验证码邮件"""
    msg = MIMEMultipart("alternative")
    msg["From"] = f"{SMTP_FROM_NAME} <{SMTP_FROM}>"
    msg["To"] = recipient
    msg["Subject"] = "Your Verification Code"

    text_content = f"Your verification code is: {code}\nIt will expire in 5 minutes."
    html_content = f"""
    <p>Your verification code is: <b>{code}</b></p>
    <p>It will expire in 5 minutes.</p>
    """

    msg.attach(MIMEText(text_content, "plain"))
    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_FROM, recipient, msg.as_string())
    print("Recipient:", recipient)

