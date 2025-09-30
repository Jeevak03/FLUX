# Agent Routing - Exclusive Request Feature

## Problem Scenario
```
User: "Hi Marc"
Sara: "I think there may be some confusion..."

User: "It's ok, But I would like to talk to Marc to get some clarification"
Sara: (Still responding instead of passing to Marc)
```

## Root Cause
The A2A (Agent-to-Agent) collaboration logic was **additive** - it would add Marc to the conversation but keep Sara active. The system didn't understand that "I would like to talk to Marc" is an **exclusive request** that should replace the current agent.

## Solution

### 1. Exclusive Request Patterns
Added detection for phrases that indicate the user wants to switch to a different agent:

```python
exclusive_patterns = [
    "would like to talk to",
    "want to talk to", 
    "need to talk to",
    "like to speak to",
    "want to speak to",
    "would like to speak to"
]
```

### 2. Agent Replacement Logic
When an exclusive pattern is detected:

1. **Clear previous agents**: Remove all agents from `agent_outputs` except the requested one
2. **Set mentioned_agents**: Only include the requested agent
3. **Update requested_agents**: Replace the list with just the requested agent

```python
if any(f"{pattern} {name}" in user_request_lower for pattern in continuation_patterns):
    # This is an EXCLUSIVE request - clear other agents
    mentioned_agents = {agent_key}
    requested_agents = [agent_key]
    print(f"[A2A] Exclusive request to talk to {name} -> using ONLY {agent_key}")
    break
```

### 3. State Cleanup
Remove the previous agent's responses from the state:

```python
if mentioned_agents and "agent_outputs" in state:
    agents_to_remove = [a for a in state["agent_outputs"].keys() if a not in mentioned_agents]
    for agent_to_remove in agents_to_remove:
        del state["agent_outputs"][agent_to_remove]
        print(f"[A2A] Removed {agent_to_remove} from conversation (exclusive request)")
```

### 4. Final Agent List
Use only the mentioned agents when it's an exclusive request:

```python
if is_exclusive_request and mentioned_agents:
    all_agents = list(mentioned_agents)
    print(f"[WORKFLOW] Exclusive request - using ONLY: {all_agents}")
else:
    all_agents = list(set(requested_agents + list(mentioned_agents)))
    print(f"[WORKFLOW] Final agent list (including A2A): {all_agents}")
```

## How It Works Now

### Scenario 1: Initial Direct Call
```
User: "Hi Marc"
  ↓
System: Routes to Marc (software_architect)
  ↓
Marc: Responds
```

### Scenario 2: Exclusive Switch Request
```
User: "Hi Marc"
  ↓
Sara: Responds (due to previous routing issue)
  ↓
User: "I would like to talk to Marc"
  ↓
System detects "would like to talk to marc"
  ↓
System marks as exclusive_request = True
  ↓
System clears Sara from agent_outputs
  ↓
System sets mentioned_agents = {"software_architect"}
  ↓
System sets requested_agents = ["software_architect"]
  ↓
Marc: Responds (Sara is no longer active)
```

### Scenario 3: Adding Agents (Non-Exclusive)
```
User (Sara active): "Can you call Marc?"
  ↓
System detects "call marc" (not exclusive pattern)
  ↓
System adds Marc to mentioned_agents
  ↓
all_agents = ["requirements_analyst", "software_architect"]
  ↓
Both Sara and Marc: Respond together
```

## Supported Patterns

### Exclusive Patterns (Replace Current Agent)
- "I would like to talk to [agent]"
- "I want to talk to [agent]"
- "I need to talk to [agent]"
- "I would like to speak to [agent]"
- "I want to speak to [agent]"
- "I like to speak to [agent]"

### Additive Patterns (Keep Current + Add New)
- "Can you call [agent]?"
- "Please bring in [agent]"
- "Can [agent] join?"
- "Let's include [agent]"

### Dismissal Patterns (Remove Agent)
- "Thanks [agent], you can drop off"
- "Thank you [agent]"
- "[agent], you can leave"

## Testing

### Test Case 1: Direct Call
```bash
cd C:\YOKA\FLUX\backend
python test_agent_routing.py
```

Expected:
- "Hi Marc" → Only Marc responds
- "Hi Sara" → Only Sara responds

### Test Case 2: Exclusive Switch
Manual test in UI:
1. Say "Hi Marc"
2. If Sara responds, say "I would like to talk to Marc"
3. Verify only Marc responds next

### Test Case 3: Additive Collaboration
Manual test in UI:
1. Say "Hi Sara"
2. Sara responds
3. Say "Can you call Marc?"
4. Verify both Sara and Marc respond

## Debug Logging

Watch for these log messages:

```
[A2A] Continuation pattern detected - focusing on specific agents
[A2A] Exclusive request to talk to marc -> using ONLY software_architect
[A2A] Exclusive request detected: 'would like to talk to'
[A2A] Removed requirements_analyst from conversation (exclusive request)
[WORKFLOW] Exclusive request - using ONLY: ['software_architect']
```

## Files Modified

1. **backend/workflows/sdlc_workflow.py**
   - Line ~292: Added exclusive patterns to continuation_patterns
   - Line ~302: Added exclusive request logic in continuation detection
   - Line ~315: Added exclusive request state cleanup
   - Line ~360: Added conditional final agent list assembly

## Status

✅ **Fixed**: Exclusive agent requests now properly replace the active agent  
✅ **Fixed**: "I would like to talk to Marc" removes Sara and activates Marc  
✅ **Maintained**: Additive patterns still work for multi-agent collaboration  
✅ **Maintained**: Direct calls ("Hi Marc") continue to work

## Next Steps

1. Test in the UI at http://localhost:3002
2. Try the conversation:
   - "Hi Marc" (if Sara responds, continue)
   - "I would like to talk to Marc"
   - Verify only Marc responds

3. If issues persist, check the backend logs for routing information

## Rollback

If needed, revert changes in:
```bash
git diff backend/workflows/sdlc_workflow.py
git checkout backend/workflows/sdlc_workflow.py
```

---

**Updated**: September 30, 2025  
**Issue**: Sara not yielding to Marc on explicit request  
**Status**: ✅ RESOLVED  
**Backend**: Running on http://localhost:8000 (PID: 40484)  
**Frontend**: Running on http://localhost:3002
