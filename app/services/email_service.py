import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.utils.config import EMAIL, APP_PASSWORD


def send_email(subject, content, to_email, cc_email=None):
    try:
        print("📧 Preparing email...")
        print("FROM:", EMAIL)
        print("TO:", to_email)
        print("CC:", cc_email)

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

        print("🔐 Connecting to Gmail SMTP...")

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        print("🔑 Logging in...")
        server.login(EMAIL, APP_PASSWORD)

        print("📤 Sending email...")
        server.sendmail(EMAIL, recipients, msg.as_string())

        server.quit()

        print("✅ EMAIL SENT SUCCESSFULLY")

    except Exception as e:
        print("❌ EMAIL ERROR:", str(e))
        raise