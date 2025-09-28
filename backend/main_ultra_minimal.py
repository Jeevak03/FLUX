# main_ultra_minimal.py
from fastapi import FastAPI

app = FastAPI(title="Ultra Minimal Server")

@app.get("/")
async def root():
    return {"message": "Ultra minimal server", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}