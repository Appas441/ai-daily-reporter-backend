from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import datetime
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

        print(f"🕒 TARGET TIME: {send_time}")

        while True:
            now = datetime.now()

            print(f"⏳ Now: {now} | Target: {send_time}")

            if now >= send_time:
                print("🚀 TIME MATCHED → SENDING EMAIL")

                try:
                    send_email(subject, content, to_email, cc_email)
                except Exception as e:
                    print("❌ SEND FAILED:", str(e))

                break

            time.sleep(5)

    except Exception as e:
        print("❌ Schedule Error:", str(e))


@router.post("/start-day")
def start_day(data: EmailRequest):
    try:
        print("📩 START REQUEST:", data)

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

    except Exception as e:
        print("❌ Start Error:", str(e))
        raise HTTPException(status_code=500, detail="Failed ❌")


@router.post("/end-day")
def end_day(data: EmailRequest):
    try:
        print("📩 END REQUEST:", data)

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
        print("❌ End Error:", str(e))
        raise HTTPException(status_code=500, detail="Failed ❌")