import asyncio
from workflows.sdlc_workflow import SDLCWorkflow

async def test_direct():
    workflow_manager = SDLCWorkflow()
    
    initial_state = {
        'user_request': 'What are the basic requirements for a todo app?',
        'current_phase': 'initial',
        'agent_outputs': {},
        'conversation_history': [],
        'project_context': {'project': 'TodoApp'},
        'next_agent': '',
        'final_response': '',
        'requested_agents': ['requirements_analyst']
    }
    
    print('Testing workflow directly...')
    count = 0
    async for state_update in workflow_manager.workflow.astream(initial_state):
        count += 1
        outputs = state_update.get('agent_outputs', {})
        print(f'Update {count}: {list(state_update.keys())}')
        print(f'  agent_outputs: {list(outputs.keys())}')
        for key, value in state_update.items():
            if key != 'agent_outputs' and key != 'conversation_history':
                print(f'  {key}: {str(value)[:100]}')
        print('---')
        if count > 3:  # Prevent infinite loop
            print('Stopping after 3 updates')
            break
    
    print('Done.')

if __name__ == "__main__":
    asyncio.run(test_direct())