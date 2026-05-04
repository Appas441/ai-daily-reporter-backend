from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.report import router

app = FastAPI(
    title="AI Daily Reporter API 🚀",
    version="1.0.0"
)

# ✅ CORS (FIXED)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://appas441.github.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   # ✅ specific origins only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ ROOT
@app.get("/")
def home():
    return {
        "message": "AI Daily Reporter API running 🚀",
        "status": "success"
    }

# ✅ HEALTH CHECK
@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "backend running"
    }

# ✅ STARTUP
@app.on_event("startup")
def startup_event():
    print("🚀 Backend started successfully")

# ✅ SHUTDOWN
@app.on_event("shutdown")
def shutdown_event():
    print("🛑 Backend shutting down")

# ✅ ROUTES
app.include_router(router)