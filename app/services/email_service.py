import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# ✅ GET ENV VARIABLES (Render uses this)
EMAIL = os.getenv("EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")


def send_email(subject, content, to_email, cc_email=None):
    try:
        # 🔍 DEBUG (VERY IMPORTANT)
        print("📧 EMAIL:", EMAIL)
        print("🔐 APP_PASSWORD:", "SET" if APP_PASSWORD else "NOT SET")
        print("📨 TO:", to_email)
        print("📨 CC:", cc_email)

        if not EMAIL or not APP_PASSWORD:
            raise Exception("Email credentials not set in environment variables")

        # ✅ CREATE MESSAGE
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

        # ✅ GMAIL SMTP
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login(EMAIL, APP_PASSWORD)

        server.sendmail(EMAIL, recipients, msg.as_string())
        server.quit()

        print("✅ EMAIL SENT SUCCESSFULLY")

    except Exception as e:
        print("❌ EMAIL ERROR:", str(e))
        raise