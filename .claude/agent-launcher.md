# NetAssist Agent Launcher

## Project: NetAssist VS Code Extension
AI-powered network engineering assistant with secure IP sanitization

## Tech Stack
- **Frontend**: TypeScript + VS Code Extension API
- **Backend**: Python + FastAPI + Pydantic
- **Specialization**: Network engineering, IP sanitization, pyATS integration
- **Infrastructure**: Docker, pytest, Jest

## Available Commands
- `/build` - Full development cycle with TDD
- `/test` - Run comprehensive test suite
- `/debug` - Network-specific debugging
- `/deploy` - Package and deploy extension

## Agent Loading Strategy

### Core Agents (Always Available)
- **architect**: VS Code extension + FastAPI architecture
- **engineer**: TypeScript/Python network engineering
- **reviewer**: Security + network compliance review

### Specialized Agents (Load on Demand)
- **network-specialist**: IP sanitization + pyATS + Cisco configs
- **api-specialist**: FastAPI endpoints + network protocols

## Agent Selection Logic

```
User Intent → Agent Selection
network config → network-specialist + engineer
sanitization bug → network-specialist + api-specialist
extension UI → engineer + architect
test failures → engineer + reviewer
deployment → architect + reviewer
```

## Performance Targets
- Agent loading: <2s
- Parallel execution: 3 agents max
- Context size: <10KB auto-loaded