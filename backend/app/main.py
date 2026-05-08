from fastapi import FastAPI
from app.api import upload, chat
from app.api.sync import router as sync_router   # ✅ FIX

app = FastAPI()

# Existing routes
app.include_router(upload.router)
app.include_router(chat.router)

# 🔥 NEW route
app.include_router(sync_router)   # ✅ FIX

@app.get("/")
def home():
    return {"message": "Backend is running"}