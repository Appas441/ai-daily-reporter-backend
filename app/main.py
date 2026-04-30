from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.report import router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://appas441.github.io",  # ✅ add this
        "https://appas441.github.io/ai-daily-reporter-frontend/",  # ✅ optional
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)