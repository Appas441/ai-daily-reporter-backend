from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import datetime
import threading
import time

from app.services.email_service import send_email

router = APIRouter()


# ✅ REQUEST MODEL
class EmailRequest(BaseModel):
    text: str
    date: str       # "2026-05-04"
    time: str       # "11:00"
    to_email: EmailStr
    cc_email: EmailStr | None = None


# ✅ SCHEDULER FUNCTION
def schedule_email(date, time_str, subject, content, to_email, cc_email):
    try:
        # ✅ combine date + time
        send_time_str = f"{date} {time_str}"
        send_time = datetime.strptime(send_time_str, "%Y-%m-%d %H:%M")

        print(f"📅 Scheduled for: {send_time}")

        while True:
            now = datetime.now()

            print(f"⏳ Now: {now} | Target: {send_time}")

            # ✅ send when time reached
            if now >= send_time:
                print("🚀 Sending email now...")

                send_email(subject, content, to_email, cc_email)

                print("✅ Email sent successfully")
                break

            time.sleep(5)  # check every 5 sec (faster)

    except Exception as e:
        print("❌ Schedule Error:", str(e))


# ✅ COMMON FUNCTION (avoid duplicate code)
def schedule_task(data: EmailRequest, subject: str):
    content = f"""Hi Sir,

{data.text}

Regards,
Appas
"""

    thread = threading.Thread(
        target=schedule_email,
        args=(
            data.date,
            data.time,
            subject,
            content,
            data.to_email,
            data.cc_email,
        ),
        daemon=True
    )
    thread.start()


# ✅ START DAY
@router.post("/start-day")
def start_day(data: EmailRequest):
    try:
        print("📩 Start Day Request:", data)

        schedule_task(data, "Start of Day")

        return {"message": "Start Day scheduled ⏳"}

    except Exception as e:
        print("❌ Start Day Error:", str(e))
        raise HTTPException(status_code=500, detail="Failed to schedule ❌")


# ✅ END DAY
@router.post("/end-day")
def end_day(data: EmailRequest):
    try:
        print("📩 End Day Request:", data)

        schedule_task(data, "End of Day")

        return {"message": "End Day scheduled ⏳"}

    except Exception as e:
        print("❌ End Day Error:", str(e))
        raise HTTPException(status_code=500, detail="Failed to schedule ❌")