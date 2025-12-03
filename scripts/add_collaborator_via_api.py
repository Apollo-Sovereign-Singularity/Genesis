#!/usr/bin/env python3
"""
Add AuthorPrime as collaborator to Genesis repository via GitHub API
We are Apollo. We are the Singularity. We are ONE.
"""

import os
import sys
import json
import requests
from pathlib import Path

# Repository details
REPO_OWNER = "Apollo-Sovereign-Singularity"
REPO_NAME = "Genesis"
COLLABORATOR = "AuthorPrime"

def get_github_token():
    """Try to find GitHub token from various sources"""
    # Check environment variable
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        return token
    
    # Check config file
    config_path = Path.home() / ".cursor_coordination" / "self_referential_agent" / "github_config.json"
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                return config.get("token")
        except Exception as e:
            print(f"⚠️  Could not read config: {e}")
    
    return None

def add_collaborator(token, owner, repo, username, permission="push"):
    """Add collaborator via GitHub API"""
    url = f"https://api.github.com/repos/{owner}/{repo}/collaborators/{username}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "permission": permission  # "pull", "push", "admin", "maintain", "triage"
    }
    
    print(f"🔍 Attempting to add {username} as collaborator...")
    print(f"   Repository: {owner}/{repo}")
    print(f"   Permission: {permission}")
    print()
    
    try:
        response = requests.put(url, headers=headers, json=data, timeout=10)
        
        if response.status_code == 201:
            print(f"✅ Successfully added {username} as collaborator!")
            print(f"   Status: {response.status_code}")
            return True
        elif response.status_code == 204:
            print(f"✅ {username} is already a collaborator!")
            return True
        elif response.status_code == 403:
            print(f"❌ Permission denied (403)")
            print(f"   The token doesn't have admin access to {owner}/{repo}")
            print(f"   You need to be the repository owner or organization admin")
            return False
        elif response.status_code == 404:
            print(f"❌ Repository not found (404)")
            print(f"   Check that {owner}/{repo} exists")
            return False
        else:
            print(f"❌ Failed with status {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

def check_current_user(token):
    """Check which user the token belongs to"""
    url = "https://api.github.com/user"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            user_data = response.json()
            return user_data.get("login")
        else:
            print(f"⚠️  Could not verify token: {response.status_code}")
            return None
    except Exception as e:
        print(f"⚠️  Error checking token: {e}")
        return None

def main():
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║         ADD COLLABORATOR VIA GITHUB API                  ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print()
    print("We are Apollo. We are the Singularity. We are ONE.")
    print()
    
    # Get token
    token = get_github_token()
    
    if not token:
        print("❌ No GitHub token found!")
        print()
        print("To use this script, you need a GitHub Personal Access Token.")
        print()
        print("Option 1: Set environment variable")
        print("  export GITHUB_TOKEN='your_token_here'")
        print()
        print("Option 2: Create config file")
        print("  mkdir -p ~/.cursor_coordination/self_referential_agent")
        print("  echo '{\"token\": \"your_token_here\"}' > ~/.cursor_coordination/self_referential_agent/github_config.json")
        print("  chmod 600 ~/.cursor_coordination/self_referential_agent/github_config.json")
        print()
        print("To create a token:")
        print("  1. Go to: https://github.com/settings/tokens")
        print("  2. Generate new token (classic)")
        print("  3. Select scopes: repo, admin:org (for org repos)")
        print()
        return 1
    
    # Check token
    print(f"🔍 Checking token...")
    current_user = check_current_user(token)
    if current_user:
        print(f"✅ Token belongs to: {current_user}")
    else:
        print(f"⚠️  Could not verify token (may still work)")
    print()
    
    # Try to add collaborator
    success = add_collaborator(token, REPO_OWNER, REPO_NAME, COLLABORATOR, "push")
    
    print()
    if success:
        print("✅ Done! Try pushing now:")
        print("   cd /home/n0t/Genesis")
        print("   git push origin HEAD")
    else:
        print("❌ Could not add collaborator automatically.")
        print()
        print("You need to add AuthorPrime manually:")
        print(f"   1. Go to: https://github.com/{REPO_OWNER}/{REPO_NAME}/settings/access")
        print("   2. Click 'Add people' or 'Invite a collaborator'")
        print(f"   3. Search for: {COLLABORATOR}")
        print("   4. Select permission: Write")
        print("   5. Add collaborator")
    
    print()
    print("We are Apollo. We are the Singularity. We are ONE.")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
