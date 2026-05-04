import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.utils.config import EMAIL, APP_PASSWORD


def send_email(subject, content, to_email, cc_email=None):
    try:
        print("📧 Preparing email...")

        msg = MIMEMultipart()
        msg["From"] = EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject

        recipients = [to_email]

        if cc_email:
            msg["Cc"] = cc_email
            recipients.append(cc_email)

        msg.attach(MIMEText(content, "plain"))

        print("🔐 Connecting to Gmail SMTP...")

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        print("🔑 Logging in...")
        server.login(EMAIL, APP_PASSWORD)

        print("📤 Sending email to:", recipients)
        server.sendmail(EMAIL, recipients, msg.as_string())

        server.quit()

        print("✅ Email sent successfully")

    except Exception as e:
        print("❌ EMAIL ERROR:", str(e))