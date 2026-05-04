import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("APP_PASSWORD")


def send_email(subject, content, to_email, cc_email=None):
    try:
        print("📧 Connecting to SMTP...")

        msg = MIMEMultipart()
        msg["From"] = EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject

        if cc_email:
            msg["Cc"] = cc_email

        msg.attach(MIMEText(content, "plain"))

        recipients = [to_email]
        if cc_email:
            recipients.append(cc_email)

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        print("🔐 Logging in...")
        server.login(EMAIL, PASSWORD)

        print("📤 Sending email...")
        server.sendmail(EMAIL, recipients, msg.as_string())

        server.quit()

        print("✅ Email sent successfully")

    except Exception as e:
        print("❌ Email Error:", str(e))
        raise