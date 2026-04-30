from fastapi import APIRouter
from pydantic import BaseModel
from app.models.log_model import Log
from app.services.email_service import send_email
from app.utils.file_handler import read_logs, write_logs

router = APIRouter()

# ✅ Request models
class StartDayRequest(BaseModel):
    text: str

class EndDayRequest(BaseModel):
    text: str


# ✅ START DAY (dynamic)
@router.post("/start-day")
def start_day(data: StartDayRequest):
    content = f"""Hi Sir,

{data.text}

Regards,
Appas
"""
    send_email("Start of Day", content)
    return {"message": "Start day email sent"}


# ✅ SAVE LOG (optional, for storage only)
@router.post("/log")
def save_log(log: Log):
    logs = read_logs()
    logs.append(log.text)
    write_logs(logs)
    return {"message": "Log saved"}


# ✅ END DAY (dynamic — uses textarea ONLY)
@router.post("/end-day")
def end_day(data: EndDayRequest):
    content = f"""Hi Sir,

{data.text}

Regards,
Appas
"""
    send_email("End of Day", content)
    return {"message": "End day email sent"}


# ✅ GET LOGS (optional)
@router.get("/logs")
def get_logs():
    return read_logs()