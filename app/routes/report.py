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
    date: str
    time: str
    to_email: EmailStr
    cc_email: EmailStr | None = None


# ✅ FINAL SCHEDULER (NO UTC CONFUSION)
def schedule_email(date, time_str, subject, content, to_email, cc_email):
    try:
        send_time = datetime.strptime(f"{date} {time_str}", "%Y-%m-%d %H:%M")

        print(f"🕒 Target Time (LOCAL): {send_time}")

        while True:
            now = datetime.now()

            print(f"⏳ Now: {now} | Target: {send_time}")

            if now >= send_time:
                print("🚀 Sending email now...")

                try:
                    send_email(subject, content, to_email, cc_email)
                    print("✅ Email sent successfully")
                except Exception as e:
                    print("❌ Email failed:", str(e))

                break

            time.sleep(5)  # faster check

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

        print("📩 Start Day Request Received:", data)

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

        print("📩 End Day Request Received:", data)

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
        print("❌ End Error:", str(e))
        raise HTTPException(status_code=500, detail="Failed ❌")