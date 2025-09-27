# NetAssist Debug Command

## Purpose
Network-specific debugging for VS Code extension and FastAPI backend issues

## Agents Required
- **engineer**: Analyze code and runtime issues
- **network-specialist**: Debug network data processing problems
- **reviewer**: Security and compliance issue analysis

## Debug Categories

### VS Code Extension Issues
```bash
# Extension activation/registration problems
engineer: Check extension.ts activation events
engineer: Validate command registration and bindings
engineer: Debug webview and UI component issues
```

### Network Sanitization Issues
```bash
# IP sanitization accuracy problems
network-specialist: Analyze sanitization patterns and edge cases
network-specialist: Debug IP mapping and restoration logic
network-specialist: Validate network entity detection accuracy
```

### FastAPI Backend Issues
```bash
# API endpoint and processing problems
engineer: Debug FastAPI routing and middleware
api-specialist: Analyze request/response processing
network-specialist: Debug network configuration parsing
```

### Integration Issues
```bash
# VS Code ↔ FastAPI communication problems
engineer: Debug HTTP client and API communication
reviewer: Analyze security and data flow issues
network-specialist: Validate end-to-end sanitization workflow
```

## Debug Procedures

### 1. Issue Identification
- Gather error logs and reproduction steps
- Identify affected components (VS Code, FastAPI, network processing)
- Determine if issue is functional, security, or performance related

### 2. Component Analysis
- **VS Code Extension**: Check activation, commands, UI state
- **FastAPI Backend**: Validate endpoints, models, processing logic
- **Network Processing**: Test sanitization accuracy and performance

### 3. Integration Testing
- Test VS Code → FastAPI communication
- Validate complete sanitization → AI → restoration workflow
- Check error handling and fallback mechanisms

### 4. Resolution
- Apply targeted fixes based on root cause analysis
- Update tests to prevent regression
- Document debugging procedures for future reference

## Debug Tools

### VS Code Extension Debugging
```bash
# Extension host debugging
F5: Launch Extension Development Host
Ctrl+Shift+I: Open Developer Tools for webview debugging
```

### FastAPI Backend Debugging
```bash
# Local development server with debugging
cd sanitization-server
uvicorn main:app --reload --log-level debug
```

### Network Data Debugging
```bash
# Test sanitization with various network configs
python simple_test.py
pytest test_sanitizer.py -v
```

## Success Criteria
- Root cause identified and documented
- Fix implemented with test coverage
- No regression in existing functionality
- Debug procedures documented for team