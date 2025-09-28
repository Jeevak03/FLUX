#!/usr/bin/env python3
"""
Test team collaboration and awareness
"""

import asyncio
import websockets
import json
from datetime import datetime

async def test_team_collaboration():
    session_id = f"team_test_{int(datetime.now().timestamp())}"
    uri = f"ws://localhost:8000/ws/{session_id}"
    
    try:
        print("🤝 Testing Team Collaboration and Agent Awareness...")
        
        async with websockets.connect(uri) as websocket:
            print("✅ Connected")
            
            # Test collaborative request that should trigger multiple agents
            test_request = {
                "request": "I need to build a user authentication system. Can Sarah gather requirements, Marcus design the architecture, and Alex implement it?",
                "requested_agents": [],  # Let the agents naturally collaborate
                "context": {
                    "projectName": "AuthSystem",
                    "technology": "React + Node.js",
                    "phase": "planning"
                }
            }
            
            print("📤 Sending collaborative request...")
            await websocket.send(json.dumps(test_request))
            
            # Listen for responses and check for team references
            responding_agents = set()
            team_mentions = []
            timeout_count = 0
            max_timeout = 20
            
            while timeout_count < max_timeout:
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    data = json.loads(response)
                    
                    if data.get('type') == 'agent_response':
                        agent = data.get('agent', 'unknown')
                        message = data.get('message', '')
                        responding_agents.add(agent)
                        
                        # Check for team member mentions
                        team_names = ['Sarah', 'Marcus', 'Alex', 'Jessica', 'David', 'Emily', 'Robert']
                        mentioned_names = [name for name in team_names if name in message]
                        if mentioned_names:
                            team_mentions.append({
                                'agent': agent,
                                'mentions': mentioned_names,
                                'snippet': message[:100] + '...' if len(message) > 100 else message
                            })
                        
                        print(f"🎯 {agent} responded: {message[:80]}...")
                        if mentioned_names:
                            print(f"   👥 Mentioned team members: {', '.join(mentioned_names)}")
                            
                except asyncio.TimeoutError:
                    timeout_count += 1
                    if timeout_count % 5 == 0:
                        print(f"⏳ Waiting for responses... ({timeout_count}s)")
            
            print(f"\n📊 Team Collaboration Results:")
            print(f"   👥 Total responding agents: {len(responding_agents)}")
            print(f"   🔗 Agents mentioning teammates: {len(team_mentions)}")
            
            if team_mentions:
                print(f"\n🤝 Team Awareness Examples:")
                for mention in team_mentions[:3]:  # Show first 3
                    print(f"   {mention['agent']} mentioned: {', '.join(mention['mentions'])}")
                    print(f"   📝 \"{mention['snippet']}\"")
                
                print("\n✅ SUCCESS: Agents now know about their teammates!")
                print("🎉 The team is working collaboratively instead of as strangers!")
                return True
            else:
                print("\n❌ Agents are still working in isolation")
                return False
        
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_team_collaboration())
    if success:
        print("\n🎊 Team Awareness Fixed!")
        print("   Now the agents know each other and collaborate naturally")
        print("   They will reference teammates by name and coordinate work")
    else:
        print("\n⚠️ Team awareness needs more work")