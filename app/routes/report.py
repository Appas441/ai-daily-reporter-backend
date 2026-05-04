from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
import threading
import time

from app.services.email_service import send_email

router = APIRouter()


# ✅ REQUEST MODEL (MATCH FRONTEND)
class EmailRequest(BaseModel):
    text: str
    date: str       # "2026-05-04"
    time: str       # "12:46"
    to_email: EmailStr
    cc_email: EmailStr | None = None


# ✅ SCHEDULER FUNCTION (IST → UTC FIXED)
def schedule_email(date, time_str, subject, content, to_email, cc_email):
    try:
        # 👉 Combine date + time
        send_time = datetime.strptime(f"{date} {time_str}", "%Y-%m-%d %H:%M")

        # 👉 Convert IST → UTC (IMPORTANT)
        send_time = send_time - timedelta(hours=5, minutes=30)

        print(f"🕒 IST TIME: {date} {time_str}")
        print(f"🌍 UTC TIME: {send_time}")

        while True:
            now = datetime.utcnow()

            print(f"⏳ Waiting... Now(UTC): {now} | Target(UTC): {send_time}")

            if now >= send_time:
                print("🚀 Sending email now...")

                send_email(subject, content, to_email, cc_email)

                print("✅ Email sent successfully")
                break

            time.sleep(10)  # check every 10 seconds

    except Exception as e:
        print("❌ Schedule Error:", str(e))


# ✅ START DAY
@router.post("/start-day")
def start_day(data: EmailRequest):
    try:
        content = f"""Hi Sir,

{data.text}

Regards,
Appas
"""

        threading.Thread(
            target=schedule_email,
            args=(
                data.date,
                data.time,
                "Start of Day",
                content,
                data.to_email,
                data.cc_email,
            ),
            daemon=True  # ✅ important for background task
        ).start()

        return {"message": "Start Day scheduled ⏳"}

    except Exception as e:
        print("❌ Start Day Error:", str(e))
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

        threading.Thread(
            target=schedule_email,
            args=(
                data.date,
                data.time,
                "End of Day",
                content,
                data.to_email,
                data.cc_email,
            ),
            daemon=True
        ).start()

        return {"message": "End Day scheduled ⏳"}

    except Exception as e:
        print("❌ End Day Error:", str(e))
        raise HTTPException(status_code=500, detail="Failed ❌")