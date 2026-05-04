from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import datetime
import threading
import time

from app.services.email_service import send_email

router = APIRouter()


# ✅ Request Model
class EmailRequest(BaseModel):
    text: str
    datetime: str  # "2026-05-04 11:00"
    to_email: EmailStr
    cc_email: EmailStr | None = None


# ✅ FUNCTION TO DELAY EMAIL
def schedule_email(send_time_str, subject, content, to_email, cc_email):
    try:
        send_time = datetime.strptime(send_time_str, "%Y-%m-%d %H:%M")
        now = datetime.now()

        delay = (send_time - now).total_seconds()

        if delay <= 0:
            print("❌ Time already passed")
            return

        print(f"⏳ Email will send in {delay} seconds")

        time.sleep(delay)

        send_email(subject, content, to_email, cc_email)

        print("✅ Email sent successfully")

    except Exception as e:
        print("Schedule Error:", e)


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
                data.datetime,
                "Start of Day",
                content,
                data.to_email,
                data.cc_email,
            ),
        ).start()

        return {"message": "Start Day scheduled ⏳"}

    except Exception as e:
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
                data.datetime,
                "End of Day",
                content,
                data.to_email,
                data.cc_email,
            ),
        ).start()

        return {"message": "End Day scheduled ⏳"}

    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed ❌")