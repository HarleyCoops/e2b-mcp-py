# LangGraph Migration Plan

## Overview

Migrating from `deepagents` to `langgraph` for a more modern, stateful agent architecture.

## Current Architecture (deepagents)

```
User Input → deepagents.create_deep_agent() → LangChain Tools → E2B Sandbox → Results
                    ↓
            - Planning via write_todos
            - Subagent spawning
            - File system management
```

## New Architecture (LangGraph)

```
User Input → LangGraph StateGraph → Tool Nodes → E2B Sandbox → Results
                    ↓
            - State-based planning
            - Conditional routing
            - Built-in memory/checkpoints
            - React-style agent loop
```

## Key Changes

### 1. Agent State Definition
Replace implicit state management with explicit TypedDict state schema:
- `messages`: Conversation history
- `plan`: Current task plan/steps
- `sandbox_info`: E2B sandbox metadata
- `next_action`: What to do next

### 2. Graph Structure
Replace deepagents orchestration with LangGraph nodes:
- **planner_node**: Analyzes task and creates execution plan
- **tool_node**: Executes tools (E2B, MCP, etc.)
- **reasoner_node**: Decides next action based on results
- **final_node**: Formats and returns final result

### 3. Conditional Routing
Use LangGraph's routing for dynamic workflows:
- Route to planner when task needs decomposition
- Route to tools when action is needed
- Route to reasoner after tool execution
- Route to END when task is complete

### 4. Advantages Over deepagents

#### State Management
- **Before**: Implicit state in conversation
- **After**: Explicit state dict with schemas

#### Planning
- **Before**: write_todos tool
- **After**: Built-in state tracking with `plan` field

#### Subagents
- **Before**: Spawning separate agents
- **After**: Graph branches with parallel execution

#### Debugging
- **Before**: Limited introspection
- **After**: LangGraph Studio compatible, checkpoints

#### Error Handling
- **Before**: Try/catch in tools
- **After**: Graph-level error nodes and retries

### 5. Preserved Features

All existing capabilities remain:
- ✅ E2B sandbox integration
- ✅ MCP server tools (GitHub, Notion)
- ✅ File system operations
- ✅ Package management
- ✅ MCP builder tools (self-extension)
- ✅ Interactive chat mode
- ✅ Single-task execution
- ✅ Deployment server support

### 6. New Capabilities

LangGraph adds:
- ✅ Persistent state across interruptions
- ✅ Human-in-the-loop approval points
- ✅ Parallel tool execution
- ✅ Time-travel debugging
- ✅ Streaming support
- ✅ Better error recovery

## Implementation Steps

### Phase 1: Core Refactor
1. ✅ Define AgentState TypedDict
2. ✅ Create graph nodes (planner, tool, reasoner)
3. ✅ Define conditional routing logic
4. ✅ Wire up E2B tools to tool node
5. ✅ Test basic workflows

### Phase 2: Advanced Features
6. ⬜ Add checkpointing for resumability
7. ⬜ Implement parallel tool execution
8. ⬜ Add human-in-the-loop nodes
9. ⬜ Streaming responses

### Phase 3: Polish
10. ⬜ Update all examples
11. ⬜ Update documentation
12. ⬜ Performance testing
13. ⬜ Deploy server compatibility

## File Changes Required

### Modified Files
- `deep_agent.py` → Complete rewrite using LangGraph
- `main.py` → Update imports (if needed)
- `examples.py` → Update imports (if needed)
- `deploy.py` → Update imports (if needed)
- `README.md` → Update architecture section
- `pyproject.toml` → Remove deepagents dependency

### New Files
- `langgraph_agent.py` → New LangGraph implementation
- `MIGRATION_PLAN.md` → This file

## Testing Strategy

1. Unit tests for each graph node
2. Integration tests with E2B sandbox
3. End-to-end tests for each example scenario
4. Performance comparison (deepagents vs langgraph)

## Rollout Plan

### Option A: Hard Cutover
- Replace deep_agent.py entirely
- Update all references
- Single PR, clean break

### Option B: Parallel Migration
- Keep deep_agent.py (rename to legacy_agent.py)
- Create langgraph_agent.py
- Gradual migration
- Dual support during transition

**Recommendation**: Option A (Hard Cutover) - cleaner, less maintenance

## Compatibility Notes

### Breaking Changes
- `create_deep_agent()` → `create_langgraph_agent()`
- No functional API changes for end users
- Same tools, same capabilities

### Migration Path for Users
```python
# Before
from deep_agent import DeepAgentE2B
agent = DeepAgentE2B()

# After
from deep_agent import DeepAgentE2B  # Same class name, new implementation
agent = DeepAgentE2B()  # Same interface
```

## Timeline Estimate

- Core refactor: 2-3 hours
- Testing: 1-2 hours
- Documentation: 1 hour
- **Total**: 4-6 hours

## Success Criteria

- ✅ All existing examples work unchanged
- ✅ Performance is equal or better
- ✅ Code is cleaner and more maintainable
- ✅ New LangGraph features are accessible
- ✅ Documentation is updated
- ✅ No regressions in functionality

## References

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangGraph Tutorials](https://langchain-ai.github.io/langgraph/tutorials/)
- [React Agent Pattern](https://langchain-ai.github.io/langgraph/tutorials/introduction/)
