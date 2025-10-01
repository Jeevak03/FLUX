import os
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {
        "message": "FLUX API Test",
        "groq_key_exists": "GROQ_API_KEY" in os.environ,
        "groq_key_length": len(os.environ.get("GROQ_API_KEY", "")),
        "all_env_vars": list(os.environ.keys())
    }

# Vercel handler
def handler(request):
    return app(request)