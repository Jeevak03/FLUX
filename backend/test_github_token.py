#!/usr/bin/env python3
"""
Test GitHub Token - Quick verification script
"""

import os
import requests
from dotenv import load_dotenv

def test_github_token():
    # Load environment variables
    load_dotenv()
    
    token = os.getenv('GITHUB_TOKEN')
    
    if not token:
        print("❌ GITHUB_TOKEN not found in .env file")
        print("Please add your GitHub token to the .env file:")
        print("GITHUB_TOKEN=your_token_here")
        return False
    
    if token == 'your_token_here':
        print("❌ Please replace 'your_token_here' with your actual GitHub token")
        return False
    
    print("🔍 Testing GitHub token...")
    
    # Test API access
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        # Test basic API access
        response = requests.get("https://api.github.com/user", headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ GitHub token is valid!")
            print(f"   👤 Username: {user_data.get('login', 'Unknown')}")
            print(f"   📧 Email: {user_data.get('email', 'Private')}")
            print(f"   🏢 Company: {user_data.get('company', 'None')}")
            print(f"   📍 Location: {user_data.get('location', 'Unknown')}")
            print(f"   📊 Public Repos: {user_data.get('public_repos', 0)}")
            print(f"   👥 Followers: {user_data.get('followers', 0)}")
            
            # Test repository access
            print("\n🔍 Testing repository access...")
            repo_response = requests.get("https://api.github.com/user/repos?per_page=5", headers=headers)
            
            if repo_response.status_code == 200:
                repos = repo_response.json()
                print(f"✅ Can access repositories! Found {len(repos)} (showing first 5)")
                for repo in repos[:3]:
                    print(f"   📂 {repo['full_name']} ({repo['language'] or 'No language'})")
                
                return True
            else:
                print(f"⚠️  Repository access limited: {repo_response.status_code}")
                return True  # Token works but limited access
                
        elif response.status_code == 401:
            print("❌ Invalid GitHub token")
            print("   Make sure you copied the token correctly")
            return False
        elif response.status_code == 403:
            print("❌ GitHub token lacks required permissions")
            print("   Make sure your token has these scopes:")
            print("   - repo (Full control of private repositories)")
            print("   - read:org (Read org membership)")
            print("   - read:user (Read user profile)")
            print("   - user:email (Read user email)")
            return False
        else:
            print(f"❌ Unexpected response: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        print("   Check your internet connection")
        return False

if __name__ == "__main__":
    print("🔑 GitHub Token Verification")
    print("=" * 30)
    
    success = test_github_token()
    
    print("\n" + "=" * 30)
    if success:
        print("🎉 Ready to use GitHub integration!")
        print("   Start your servers and go to the GitHub tab")
    else:
        print("❌ Please fix the GitHub token issue above")
        print("   Get your token from: https://github.com/settings/tokens")