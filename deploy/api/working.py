from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.parse

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL path
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        # Enable CORS
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        # Get GROQ API key
        groq_api_key = os.environ.get("GROQ_API_KEY")
        groq_client = None
        
        # Try to initialize Groq client
        if groq_api_key:
            try:
                from groq import Groq
                groq_client = Groq(api_key=groq_api_key)
            except Exception as e:
                groq_client = None
        
        # Response data
        response_data = {
            "message": "FLUX Multi-Agent System API",
            "status": "running",
            "path": path,
            "method": "GET",
            "groq_configured": groq_api_key is not None,
            "groq_client_ready": groq_client is not None,
            "groq_key_length": len(groq_api_key) if groq_api_key else 0,
            "debug": {
                "email_used": "ilamvazhuthi.pro@gmail.com",
                "environment": os.environ.get("VERCEL_ENV", "unknown"),
                "vercel": os.environ.get("VERCEL", "false")
            }
        }
        
        # Handle different endpoints
        if path.endswith('/health'):
            response_data.update({
                "endpoint": "health",
                "timestamp": "2025-10-01T00:00:00Z",
                "healthy": True
            })
        elif path.endswith('/agents'):
            response_data.update({
                "endpoint": "agents",
                "agents": {
                    "sara": {"name": "Sara (Requirements Analyst)", "status": "online"},
                    "marc": {"name": "Marc (Software Architect)", "status": "online"},
                    "alex": {"name": "Alex (Developer)", "status": "online"},
                    "jess": {"name": "Jess (QA Tester)", "status": "online"},
                    "dave": {"name": "Dave (DevOps Engineer)", "status": "online"},
                    "emma": {"name": "Emma (Project Manager)", "status": "online"},
                    "robt": {"name": "Robt (Security Expert)", "status": "online"}
                }
            })
        else:
            response_data.update({
                "endpoint": "root",
                "available_endpoints": ["/api/", "/api/health", "/api/agents", "/api/chat"]
            })
        
        # Send response
        self.wfile.write(json.dumps(response_data, indent=2).encode())
        
    def do_POST(self):
        # Handle POST requests (for chat)
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        try:
            request_data = json.loads(post_data.decode())
            message = request_data.get('message', '')
            
            response_data = {
                "message": "Chat endpoint working",
                "received_message": message,
                "agent": "Sara (System)",
                "response": f"Hello! I received your message: '{message}'. The GROQ API integration is being set up.",
                "timestamp": "2025-10-01T00:00:00Z",
                "groq_configured": os.environ.get("GROQ_API_KEY") is not None
            }
            
            self.wfile.write(json.dumps(response_data, indent=2).encode())
            
        except Exception as e:
            error_response = {
                "error": str(e),
                "message": "Error processing POST request"
            }
            self.wfile.write(json.dumps(error_response, indent=2).encode())
            
    def do_OPTIONS(self):
        # Handle preflight CORS requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(b'')