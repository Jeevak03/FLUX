# FLUX API - Ultra Simple for Vercel Testing
import os
import json

# Environment check
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
groq_client = None

# Try to initialize Groq client
if GROQ_API_KEY:
    try:
        from groq import Groq
        groq_client = Groq(api_key=GROQ_API_KEY)
    except Exception as e:
        groq_client = None

# Simple handler function for Vercel
def handler(event, context):
    try:
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({
                "message": "FLUX Multi-Agent System",
                "status": "running",
                "groq_configured": GROQ_API_KEY is not None,
                "groq_client_ready": groq_client is not None,
                "groq_key_length": len(GROQ_API_KEY) if GROQ_API_KEY else 0,
                "debug": {
                    "email_used": "ilamvazhuthi.pro@gmail.com",
                    "environment": os.environ.get("VERCEL_ENV", "unknown")
                }
            })
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }