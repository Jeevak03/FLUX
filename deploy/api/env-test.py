import os

def handler(request):
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": {
            "message": "FLUX API Debug",
            "groq_key_exists": "GROQ_API_KEY" in os.environ,
            "groq_key_length": len(os.environ.get("GROQ_API_KEY", "")),
            "all_env_keys": list(os.environ.keys())
        }
    }