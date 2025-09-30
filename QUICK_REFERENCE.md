# FLUX Multi-Agent System - Quick Reference

## System Status
- **Backend**: http://localhost:8000 (PID: 40484)
- **Frontend**: http://localhost:3002
- **Status**: ✅ Both Running

## Agent Roster

| Agent | Name | Short Name | Role |
|-------|------|------------|------|
| requirements_analyst | Sara/Sarah | S | Requirements Analyst |
| software_architect | Marc/Marcus | M | Software Architect |
| developer | Alex/Alexander | A | Senior Developer |
| qa_tester | Jess/Jessica | J | QA Engineer |
| devops_engineer | Dave/David | D | DevOps Engineer |
| project_manager | Emma/Emily | E | Project Manager |
| security_expert | Robt/Robert/Rob | R | Security Expert |

## How to Call Agents

### Direct Call (Single Agent Only)
```
"Hi Marc"
"Hello Alex"
"Hey Jess"
```
→ Result: Only the called agent responds

### Exclusive Switch (Replace Current Agent)
```
"I would like to talk to Marc"
"I want to speak to Alex"
"I need to talk to Jess"
```
→ Result: Current agent is removed, new agent responds

### Add Agent (Multi-Agent Collaboration)
```
"Can you call Marc?"
"Please bring in Alex"
"Let's include Jess"
```
→ Result: New agent joins, previous agents remain

### Dismiss Agent
```
"Thanks Marc, you can drop off"
"Thank you Sara"
```
→ Result: Named agent is removed from conversation

## Common Scenarios

### Scenario A: Start Fresh with One Agent
```
You: "Hi Marc"
Marc: [responds about architecture]
```

### Scenario B: Switch Agents
```
You: "Hi Sara"
Sara: [responds about requirements]
You: "I would like to talk to Marc instead"
Marc: [responds about architecture]
(Sara is now inactive)
```

### Scenario C: Build a Team
```
You: "Hi Sara"
Sara: [responds]
You: "Can you call Marc?"
Sara: [responds]
Marc: [responds]
You: "Let's also bring in Alex"
Sara: [responds]
Marc: [responds]
Alex: [responds]
```

### Scenario D: Reduce Team
```
You: "Thanks Sara, you can drop off"
(Sara is removed)
Marc: [continues]
Alex: [continues]
```

## Troubleshooting

### Problem: Wrong agent responds
**Check**:
1. Are you using exact name? ("Marc" not "Mark")
2. Is the greeting at the start? ("Hi Marc" not "Marc, hi")
3. Check backend logs for routing messages

**Fix**:
```
You: "I would like to talk to [correct agent name]"
```

### Problem: Multiple agents respond when you want one
**Check**:
1. Were agents already active from previous messages?
2. Did you use additive language? ("call Marc" adds, doesn't replace)

**Fix**:
```
You: "Thanks everyone except Marc"
You: "I would like to talk to Marc"
```

### Problem: No response
**Check**:
1. Is backend running? Check http://localhost:8000/health
2. Is frontend running? Check http://localhost:3002
3. Is WebSocket connected? (Check browser console)

**Fix**:
Restart servers:
```powershell
# Stop
taskkill /F /PID 40484
Ctrl+C in frontend terminal

# Start
cd C:\YOKA\FLUX\backend
python run_full_server.py

cd C:\YOKA\FLUX\frontend
npm run dev
```

## Agent Expertise

### Sara (Requirements Analyst)
- Gathering requirements
- User stories
- Acceptance criteria
- Business logic
- Feature specifications

### Marc (Software Architect)
- System design
- Architecture patterns
- Technology stack
- Scalability
- System integration
- Technical decisions

### Alex (Developer)
- Code implementation
- Best practices
- Code reviews
- Debugging
- Feature development
- Technical implementation

### Jess (QA Tester)
- Test planning
- Quality assurance
- Bug identification
- Test automation
- Regression testing
- Quality metrics

### Dave (DevOps Engineer)
- Deployment strategies
- CI/CD pipelines
- Infrastructure
- Monitoring
- Performance optimization
- Cloud services

### Emma (Project Manager)
- Project planning
- Timeline management
- Resource allocation
- Risk management
- Stakeholder communication
- Progress tracking

### Robt (Security Expert)
- Security assessment
- Vulnerability analysis
- Security best practices
- Compliance
- Threat modeling
- Security testing

## Example Conversations

### Getting Architecture Help
```
You: "Hi Marc, I need help designing a microservices architecture"
Marc: [provides architecture guidance]
```

### Requirements + Architecture
```
You: "Hi Sara, I need to gather requirements for a new feature"
Sara: [helps with requirements]
You: "Can you call Marc to validate the technical feasibility?"
Sara: [comments on requirements]
Marc: [validates technical feasibility]
```

### Full SDLC Flow
```
You: "Hi Sara, let's plan a new authentication system"
Sara: [gathers requirements]
You: "Please bring in Marc for architecture"
Sara: [continues requirements]
Marc: [proposes architecture]
You: "Let's get Alex to review the implementation approach"
Sara: [requirements perspective]
Marc: [architecture perspective]
Alex: [implementation perspective]
You: "Thanks Sara, you can drop off. Marc and Alex, let's continue"
Marc: [continues]
Alex: [continues]
```

## Quick Command Reference

| What You Want | Say This |
|--------------|----------|
| Talk to one agent | "Hi [name]" |
| Switch agents | "I would like to talk to [name]" |
| Add an agent | "Can you call [name]?" |
| Remove an agent | "Thanks [name], drop off" |
| Remove all but one | "I would like to talk to [name]" |
| Check who's active | (Look at conversation history) |

## Files for Reference

- **Agent Routing Logic**: `backend/workflows/sdlc_workflow.py`
- **Main Backend**: `backend/main.py`
- **Frontend UI**: `frontend/components/EnhancedChat/EnhancedChatInterface.tsx`
- **Documentation**: `AGENT_ROUTING_FIX.md`, `EXCLUSIVE_REQUEST_FIX.md`
- **Tests**: `backend/test_agent_routing.py`

---

**Last Updated**: September 30, 2025  
**System Version**: FLUX v1.0  
**Status**: ✅ Operational
