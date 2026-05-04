from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import datetime

from app.services.email_service import send_email

router = APIRouter()


# ✅ REQUEST MODEL
class EmailRequest(BaseModel):
    text: str
    date: str
    time: str
    to_email: EmailStr
    cc_email: EmailStr | None = None


# ✅ SEND EMAIL DIRECTLY (NO THREAD)
def process_email(date, time_str, subject, content, to_email, cc_email):
    try:
        send_time = datetime.strptime(f"{date} {time_str}", "%Y-%m-%d %H:%M")
        now = datetime.now()

        print(f"🕒 Now: {now}")
        print(f"📅 Scheduled: {send_time}")

        if now >= send_time:
            print("🚀 Sending email immediately...")
        else:
            print("⚠️ Time is future → sending now (Render free limitation)")

        send_email(subject, content, to_email, cc_email)

        print("✅ Email sent successfully")

    except Exception as e:
        print("❌ Email Error:", str(e))
        raise


# ✅ START DAY
@router.post("/start-day")
def start_day(data: EmailRequest):
    try:
        content = f"""Hi Sir,

{data.text}

Regards,
Appas
"""

        print("📩 Start Request:", data)

        process_email(
            data.date,
            data.time,
            "Start of Day",
            content,
            data.to_email,
            data.cc_email,
        )

        return {"message": "Start Email Sent ✅"}

    except Exception as e:
        print("❌ Start Error:", str(e))
        raise HTTPException(status_code=500, detail="Failed ❌")


# ✅ END DAY
@router.post("/end-day")
def end_day(data: EmailRequest):
    try:
        content = f"""Hi Sir,

{data.text}

Regards,
Appas
"""

        print("📩 End Request:", data)

        process_email(
            data.date,
            data.time,
            "End of Day",
            content,
            data.to_email,
            data.cc_email,
        )

        return {"message": "End Email Sent ✅"}

    except Exception as e:
        print("❌ End Error:", str(e))
        raise HTTPException(status_code=500, detail="Failed ❌")