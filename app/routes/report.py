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
        send_time_str = f"{date} {time_str}"
        send_time = datetime.strptime(send_time_str, "%Y-%m-%d %H:%M")

        while True:
            now = datetime.now()

            # DEBUG LOG
            print(f"⏳ Waiting... Now: {now} | Target: {send_time}")

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
            daemon=True  # ✅ important
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