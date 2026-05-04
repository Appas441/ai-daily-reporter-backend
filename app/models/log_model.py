from pydantic import BaseModel, Field


class Log(BaseModel):
    text: str = Field(..., min_length=1)