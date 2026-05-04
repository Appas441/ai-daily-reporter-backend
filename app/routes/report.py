from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
import threading
import time

from app.services.email_service import send_email

router = APIRouter()


class EmailRequest(BaseModel):
    text: str
    date: str
    time: str
    to_email: EmailStr
    cc_email: EmailStr | None = None


def schedule_email(date, time_str, subject, content, to_email, cc_email):
    try:
        send_time = datetime.strptime(f"{date} {time_str}", "%Y-%m-%d %H:%M")

        # ✅ IST → UTC
        send_time = send_time - timedelta(hours=5, minutes=30)

        print(f"🕒 IST: {date} {time_str}")
        print(f"🌍 UTC: {send_time}")

        while True:
            now = datetime.utcnow()

            if now >= send_time:
                print("🚀 Sending email now...")
                send_email(subject, content, to_email, cc_email)
                break

            time.sleep(10)

    except Exception as e:
        print("❌ Schedule Error:", str(e))


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
            daemon=True
        ).start()

        return {"message": "Start Day scheduled ⏳"}

    except Exception:
        raise HTTPException(status_code=500, detail="Failed ❌")


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

    except Exception:
        raise HTTPException(status_code=500, detail="Failed ❌")