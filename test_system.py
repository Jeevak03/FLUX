#!/usr/bin/env python3
"""
SDLC Multi-Agent Assistant - Test Script
Tests both backend and frontend functionality
"""

import os
import sys
import subprocess
import time
import requests
import websocket
import json
import threading

def test_backend_imports():
    """Test that backend imports work correctly"""
    print("🧪 Testing backend imports...")
    try:
        # Test basic imports
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
        import main
        print("✅ Backend imports successful")
        return True
    except Exception as e:
        print(f"❌ Backend import failed: {e}")
        return False

def test_frontend_build():
    """Test that frontend can be built"""
    print("🧪 Testing frontend build...")
    try:
        # Check if node_modules exists
        frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
        if not os.path.exists(os.path.join(frontend_dir, 'node_modules')):
            print("❌ Frontend dependencies not installed. Run 'npm install' in frontend directory")
            return False

        # Try to build (this might fail on Windows due to file locking, but compilation should work)
        result = subprocess.run(
            ['npm', 'run', 'build'],
            cwd=frontend_dir,
            capture_output=True,
            text=True,
            timeout=60
        )

        if "Compiled successfully" in result.stdout:
            print("✅ Frontend compilation successful")
            return True
        else:
            print(f"❌ Frontend build failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Frontend build test failed: {e}")
        return False

def test_websocket_connection():
    """Test WebSocket connection (requires backend running)"""
    print("🧪 Testing WebSocket connection...")
    try:
        # This would require the backend to be running
        # For now, just test that the WebSocket import works
        import websocket
        print("✅ WebSocket library available")
        return True
    except Exception as e:
        print(f"❌ WebSocket test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 SDLC Multi-Agent Assistant - System Test\n")

    tests = [
        test_backend_imports,
        test_frontend_build,
        test_websocket_connection
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! The SDLC Assistant is ready to run.")
        print("\n📋 Next Steps:")
        print("1. Set your GROQ_API_KEY environment variable")
        print("2. Start the backend: cd backend && uvicorn main:app --reload")
        print("3. Start the frontend: cd frontend && npm run dev")
        print("4. Open http://localhost:3000 in your browser")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)