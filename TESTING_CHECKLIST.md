# FLUX Multi-Agent System - Testing Checklist

## Pre-Testing Verification

### ✅ System Status
- [ ] Backend running on http://localhost:8000
  - Check: `curl http://localhost:8000/health` or open in browser
  - Expected: `{"status":"healthy"}`
- [ ] Frontend running on http://localhost:3002
  - Open: http://localhost:3002
  - Expected: Chat interface loads
- [ ] WebSocket connection active
  - Check browser console for connection messages
  - Expected: No WebSocket errors

### ✅ Environment Check
```powershell
# Backend check
Get-Process | Where-Object {$_.Id -eq 40484}

# Frontend check
Get-NetTCPConnection -LocalPort 3002
```

---

## Test Suite 1: Direct Agent Calls

### Test 1.1: Call Marc Directly
**Input**: `"Hi Marc, what's your role?"`

**Expected Behavior**:
- ✅ Only Marc responds
- ✅ No other agents join
- ✅ Response mentions architecture

**Backend Logs to Check**:
```
[ROUTE] Direct greeting to: software_architect
[WORKFLOW] called_agent is set to: software_architect
```

**Pass Criteria**: Only Marc responds, no Sara

---

### Test 1.2: Call Sara Directly
**Input**: `"Hello Sara, what do you do?"`

**Expected Behavior**:
- ✅ Only Sara responds
- ✅ No other agents join
- ✅ Response mentions requirements

**Backend Logs to Check**:
```
[ROUTE] Direct greeting to: requirements_analyst
[WORKFLOW] called_agent is set to: requirements_analyst
```

**Pass Criteria**: Only Sara responds, no Marc

---

### Test 1.3: Call Alex Directly
**Input**: `"Hey Alex, tell me about yourself"`

**Expected Behavior**:
- ✅ Only Alex responds
- ✅ Response mentions development

**Pass Criteria**: Single agent response

---

## Test Suite 2: Exclusive Agent Switching

### Test 2.1: Switch from Sara to Marc
**Steps**:
1. Input: `"Hi Sara"`
2. Verify: Sara responds
3. Input: `"I would like to talk to Marc"`
4. Verify: Only Marc responds (Sara should NOT respond)

**Expected Behavior**:
- ✅ Sara responds to initial greeting
- ✅ After exclusive request, only Marc responds
- ✅ Sara is removed from active agents

**Backend Logs to Check**:
```
[A2A] Detected agent mention: software_architect
[A2A] Exclusive request detected (pattern: 'would like to talk to')
[WORKFLOW] Exclusive request to talk to agent: software_architect
[WORKFLOW] Removed requirements_analyst from conversation
[WORKFLOW] Exclusive request - using ONLY mentioned agents
```

**Pass Criteria**: 
- Sara responds to first message
- Only Marc responds to second message
- No Sara in second response

---

### Test 2.2: Switch from Marc to Alex
**Steps**:
1. Input: `"Hi Marc"`
2. Verify: Marc responds
3. Input: `"I want to talk to Alex instead"`
4. Verify: Only Alex responds

**Expected Behavior**:
- ✅ Marc deactivated
- ✅ Alex activated
- ✅ Single agent response

**Backend Logs to Check**:
```
[A2A] Exclusive request detected (pattern: 'want to talk to')
[WORKFLOW] Removed software_architect from conversation
```

**Pass Criteria**: Clean agent switch

---

### Test 2.3: Multiple Exclusive Switches
**Steps**:
1. Input: `"Hi Sara"`
2. Input: `"I would like to talk to Marc"`
3. Input: `"Actually, I need to talk to Alex"`
4. Input: `"Let me speak to Jess"`

**Expected Behavior**:
- ✅ Each step shows only the newly requested agent
- ✅ Previous agents are removed
- ✅ No accumulation of agents

**Pass Criteria**: Only current agent responds at each step

---

## Test Suite 3: Additive Collaboration

### Test 3.1: Add Agent to Conversation
**Steps**:
1. Input: `"Hi Sara"`
2. Verify: Sara responds
3. Input: `"Can you call Marc?"`
4. Verify: Both Sara AND Marc respond

**Expected Behavior**:
- ✅ Sara continues responding
- ✅ Marc joins the conversation
- ✅ Both agents provide perspectives

**Backend Logs to Check**:
```
[A2A] Detected agent mention: software_architect
[COLLAB] No exclusive pattern detected - additive collaboration
[WORKFLOW] Final agent list includes: requirements_analyst, software_architect
```

**Pass Criteria**: Both agents respond

---

### Test 3.2: Build Three-Agent Team
**Steps**:
1. Input: `"Hi Sara, plan a feature"`
2. Input: `"Please bring in Marc for architecture"`
3. Input: `"Let's also include Alex for implementation"`

**Expected Behavior**:
- ✅ Sara responds (step 1)
- ✅ Sara + Marc respond (step 2)
- ✅ Sara + Marc + Alex respond (step 3)

**Pass Criteria**: Progressive team building

---

### Test 3.3: Distinguish Additive vs Exclusive
**Steps**:
1. Input: `"Hi Sara"`
2. Input: `"Can you call Marc?"` (should add Marc)
3. Input: `"I want to talk to Alex"` (should replace with Alex)

**Expected Behavior**:
- ✅ Step 2: Sara + Marc
- ✅ Step 3: Only Alex (Sara and Marc removed)

**Pass Criteria**: Correct pattern detection

---

## Test Suite 4: Agent Dismissal

### Test 4.1: Dismiss One Agent
**Steps**:
1. Input: `"Hi Sara"`
2. Input: `"Can you call Marc?"`
3. Verify: Both respond
4. Input: `"Thanks Sara, you can drop off"`
5. Verify: Only Marc responds

**Expected Behavior**:
- ✅ Sara removed after dismissal
- ✅ Marc continues

**Backend Logs to Check**:
```
[A2A] Detected dismissal of agent: requirements_analyst
[WORKFLOW] Removed requirements_analyst from conversation
```

**Pass Criteria**: Correct agent removed

---

### Test 4.2: Dismiss Multiple Agents
**Steps**:
1. Build team: Sara, Marc, Alex
2. Input: `"Thanks Sara and Marc"`
3. Verify: Only Alex responds

**Expected Behavior**:
- ✅ Multiple agents removed
- ✅ Remaining agent continues

**Pass Criteria**: Selective dismissal works

---

## Test Suite 5: Edge Cases

### Test 5.1: Ambiguous Input
**Input**: `"I want to discuss architecture"`

**Expected Behavior**:
- ✅ System handles gracefully
- ✅ No unexpected agent activation
- ✅ Prompt for clarification or use context

**Pass Criteria**: No crashes or wrong routing

---

### Test 5.2: Typo in Name
**Input**: `"Hi Mark"` (should be "Marc")

**Expected Behavior**:
- ✅ Agent name not recognized
- ✅ System handles gracefully
- ✅ Possible fallback or clarification request

**Pass Criteria**: No error, graceful handling

---

### Test 5.3: Multiple Names in One Message
**Input**: `"Hi Sara, can Marc help too?"`

**Expected Behavior**:
- ✅ Direct call to Sara (Hi Sara)
- ✅ Marc also mentioned, but Sara has priority
- ✅ Clear routing decision

**Pass Criteria**: Predictable behavior

---

### Test 5.4: Conversation Continuity
**Steps**:
1. Input: `"Hi Marc, design an API"`
2. Marc responds with design
3. Input: `"What about scalability?"` (no agent name)

**Expected Behavior**:
- ✅ Marc continues the conversation
- ✅ Context maintained
- ✅ No need to re-greet

**Pass Criteria**: Natural conversation flow

---

## Test Suite 6: Performance & Stability

### Test 6.1: Response Time
**Measure**:
- Time from message send to first response
- Time for multi-agent responses

**Expected**:
- ✅ Single agent: < 5 seconds
- ✅ Multi-agent: < 10 seconds
- ✅ No timeouts

**Pass Criteria**: Acceptable latency

---

### Test 6.2: WebSocket Stability
**Test**:
- Send 10 messages in sequence
- Check for connection drops
- Monitor browser console

**Expected**:
- ✅ No disconnections
- ✅ All messages processed
- ✅ No WebSocket errors

**Pass Criteria**: Stable connection

---

### Test 6.3: Long Conversation
**Test**:
- Have 20+ message conversation
- Switch agents multiple times
- Build and dismiss teams

**Expected**:
- ✅ No memory leaks
- ✅ Consistent performance
- ✅ State management works

**Pass Criteria**: No degradation

---

## Test Suite 7: UI/UX Validation

### Test 7.1: Message Display
**Check**:
- ✅ User messages styled correctly (blue bubble, right-aligned)
- ✅ Agent messages styled correctly (gray bubble, left-aligned)
- ✅ Agent avatars/names displayed
- ✅ Timestamps present

**Pass Criteria**: Claude-style clean interface

---

### Test 7.2: Input Field
**Check**:
- ✅ Text input works smoothly
- ✅ Enter key sends message
- ✅ Shift+Enter creates new line
- ✅ Input clears after send

**Pass Criteria**: Smooth input experience

---

### Test 7.3: Visual Feedback
**Check**:
- ✅ Loading indicator while waiting for response
- ✅ Clear indication of active agents
- ✅ Smooth scrolling to new messages
- ✅ No UI freezing

**Pass Criteria**: Responsive UI

---

## Critical Test: Original Bug Fix

### Test 8.1: The Original Issue
**Steps** (replicate original bug report):
1. Input: `"Hi Marc"`
2. **VERIFY**: Sara does NOT respond
3. **VERIFY**: Only Marc responds

**Expected Behavior**:
- ✅ Marc responds
- ✅ Sara does NOT respond
- ✅ No wrong agent activation

**Backend Logs to Check**:
```
[ROUTE] Direct greeting to: software_architect
[WORKFLOW] called_agent is set to: software_architect
[WORKFLOW] ONLY software_architect will respond
```

**THIS IS THE CRITICAL TEST - MUST PASS**

---

### Test 8.2: The Reported Issue
**Steps** (the issue user reported):
1. Input: `"Hi Sara"`
2. Sara responds
3. Input: `"I would like to talk to Marc"`
4. **VERIFY**: Only Marc responds
5. **VERIFY**: Sara does NOT respond

**Expected Behavior**:
- ✅ Exclusive request recognized
- ✅ Sara removed from active agents
- ✅ Only Marc responds
- ✅ No Sara in response

**THIS IS THE SECOND CRITICAL TEST - MUST PASS**

---

## Debugging Guide

### If Test Fails

#### Symptom: Wrong agent responds
**Debug Steps**:
1. Check backend logs for routing messages
2. Look for `[ROUTE]`, `[A2A]`, `[COLLAB]` prefixes
3. Verify regex pattern matching
4. Check `called_agent` state variable

**Log Commands**:
```powershell
# Watch backend logs in real-time
# (already visible in backend terminal)
```

---

#### Symptom: Multiple agents respond when expecting one
**Debug Steps**:
1. Check for `[A2A]` messages indicating collaboration detection
2. Look for "Exclusive request" vs "additive collaboration" logs
3. Verify `is_exclusive_request` flag
4. Check final agent list assembly

**Key Logs**:
```
[A2A] Exclusive request detected (pattern: '...')
[WORKFLOW] Exclusive request - using ONLY mentioned agents
```

---

#### Symptom: Agent not responding at all
**Debug Steps**:
1. Check WebSocket connection (browser console)
2. Verify backend received message (logs)
3. Check for errors in agent initialization
4. Verify agent name spelling

**Quick Fix**:
- Refresh browser page
- Check backend terminal for errors
- Verify servers are running

---

#### Symptom: UI issues
**Debug Steps**:
1. Open browser console (F12)
2. Check for JavaScript errors
3. Verify WebSocket connection
4. Check network tab for failed requests

**Quick Fix**:
- Hard refresh: Ctrl+Shift+R
- Clear browser cache
- Restart frontend server

---

## Test Results Template

```markdown
## Test Session: [Date/Time]

### Environment
- Backend: [Running/Not Running] - PID: [40484]
- Frontend: [Running/Not Running] - Port: [3002]
- Browser: [Chrome/Firefox/Edge]

### Test Results

#### Test 1.1: Call Marc Directly
- Status: [PASS/FAIL]
- Notes: [Any observations]

#### Test 2.1: Switch from Sara to Marc
- Status: [PASS/FAIL]
- Notes: [Critical - original bug]
- Backend Logs: [Paste relevant logs]

#### Test 8.1: Original Bug Fix
- Status: [PASS/FAIL]
- Marc responds: [YES/NO]
- Sara responds: [YES/NO - should be NO]

#### Test 8.2: Exclusive Request
- Status: [PASS/FAIL]
- Sara removed: [YES/NO - should be YES]
- Only Marc responds: [YES/NO - should be YES]

### Overall Assessment
- Critical Tests Passed: [X/2]
- Total Tests Passed: [X/Y]
- Blockers: [List any critical issues]
- Ready for Production: [YES/NO]

### Issues Found
1. [Issue description]
   - Severity: [Critical/High/Medium/Low]
   - Steps to reproduce: [...]
   - Expected: [...]
   - Actual: [...]

### Next Steps
- [ ] [Action item 1]
- [ ] [Action item 2]
```

---

## Quick Test Commands

### Health Check
```powershell
# Backend
curl http://localhost:8000/health

# Frontend
curl http://localhost:3002
```

### Log Monitoring
Backend logs automatically visible in terminal where `run_full_server.py` is running.

### Server Restart (if needed)
```powershell
# Stop backend
taskkill /F /PID 40484

# Stop frontend
# Press Ctrl+C in frontend terminal

# Start backend
cd C:\YOKA\FLUX\backend
python run_full_server.py

# Start frontend
cd C:\YOKA\FLUX\frontend
npm run dev
```

---

## Success Criteria

### Must Pass (Critical)
- ✅ Test 8.1: "Hi Marc" → Only Marc responds
- ✅ Test 8.2: "I would like to talk to Marc" → Sara removed, only Marc responds
- ✅ Test 1.x: All direct calls work correctly
- ✅ Test 2.x: All exclusive switches work correctly

### Should Pass (Important)
- ✅ Test 3.x: Additive collaboration works
- ✅ Test 4.x: Agent dismissal works
- ✅ Test 6.x: Performance acceptable
- ✅ Test 7.x: UI works smoothly

### Nice to Have (Enhancement)
- ✅ Test 5.x: Edge cases handled gracefully
- ✅ All UI polish working perfectly

---

## Ready to Test?

1. ✅ Verify servers running
2. ✅ Open http://localhost:3002
3. ✅ Start with Test 8.1 (critical)
4. ✅ Then Test 8.2 (critical)
5. ✅ Continue with other tests
6. ✅ Document results

**Go to**: http://localhost:3002

**First test**: `"Hi Marc, what's your role?"`

**Expected**: Only Marc responds, no Sara

**Let's go! 🚀**
