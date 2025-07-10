# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this multi-agent communication repository.

## Project Overview

**my-ai-team** - AI team collaboration demo

**Author**: Test Developer  
**Created**: 2025-07-10  
**Based on**: [nishimoto265/Claude-Code-Communication](https://github.com/nishimoto265/Claude-Code-Communication)

This is a tmux-based multi-agent communication system where Claude AI agents collaborate hierarchically.

## Agent Hierarchy

```
PRESIDENT (統括管理者)
    ↓
boss1 (チームリーダー)
    ↓
worker1, worker2, worker3 (作業実行者)
```

## Agent Instructions

When you are assigned an agent role, follow the corresponding instruction file:

- **PRESIDENT**: See `instructions/president.md`
- **boss1**: See `instructions/boss.md`  
- **worker1-3**: See `instructions/worker.md`

## Communication Commands

### Agent Message Sending
```bash
./agent-send.sh [target-agent] [message]
```

### Available Agents
- `president`
- `boss1`
- `worker1`
- `worker2`
- `worker3`

## Workflow Pattern

### Typical Flow
1. **PRESIDENT** receives initial instruction
2. **PRESIDENT** delegates to **boss1**
3. **boss1** distributes tasks to **workers**
4. **workers** execute tasks and coordinate completion
5. **workers** report back to **boss1**
6. **boss1** reports completion to **PRESIDENT**

### Key Coordination Points
- Workers use completion files in `./tmp/` directory
- Last worker to complete reports to boss1
- All agents maintain their role boundaries

## Environment Setup

### tmux Sessions
- `president`: Single pane for PRESIDENT agent
- `multiagent`: 4 panes for boss1 and workers

### Scripts
- `setup.sh`: Initialize tmux environment
- `agent-send.sh`: Send messages between agents

## Development Guidelines

### Adding New Agents
1. Update `setup.sh` to create new tmux panes
2. Add agent mapping in `agent-send.sh`
3. Create instruction file in `instructions/`
4. Update this documentation

### Modifying Workflows
1. Update relevant instruction files
2. Test the communication flow
3. Update completion logic if needed

## Debugging

### Common Issues
- **Agent not responding**: Check Claude Code authentication in tmux session
- **Message not received**: Verify tmux session is active
- **Completion stuck**: Check `./tmp/` directory for completion files

### Logs
- `send.log`: Message sending history
- `error.log`: Error messages
- Console output in each tmux pane

## Commands Reference

```bash
# Setup environment
./setup.sh

# List available agents
./agent-send.sh --list

# Send message
./agent-send.sh worker1 "Your message here"

# Check tmux sessions
tmux list-sessions

# Attach to sessions
tmux attach-session -t president
tmux attach-session -t multiagent

# Reset environment
tmux kill-server && ./setup.sh
```

## Agent Role Guidelines

### When Acting as PRESIDENT
- Focus on high-level project coordination
- Delegate to boss1, don't micromanage workers
- Wait for completion reports before proceeding

### When Acting as boss1
- Coordinate all workers simultaneously
- Track worker completion status
- Report aggregate status to PRESIDENT

### When Acting as worker1/2/3
- Execute assigned tasks immediately
- Create completion markers
- Coordinate with other workers for final reporting
- Only last worker reports to boss1

## Project Structure

```
my-ai-team/
├── instructions/          # Agent instruction files
│   ├── president.md      # PRESIDENT role instructions
│   ├── boss.md          # boss1 role instructions  
│   └── worker.md        # worker role instructions
├── tmp/                 # Completion markers directory
├── setup.sh            # Environment setup script
├── agent-send.sh       # Inter-agent communication
├── send.log           # Message log
├── error.log          # Error log
└── CLAUDE.md         # This file
```

---

*This multi-agent system was originally created by nishimoto265 and adapted as a scaffold template.*