# NetAssist Build Command

## Purpose
Complete TDD development cycle for VS Code extension with FastAPI backend

## Agents Required
- **architect**: Design system architecture
- **engineer**: Implement TypeScript + Python code
- **network-specialist**: Network-specific features

## Execution Strategy
**Parallel Phase 1** (Architecture):
- architect: Design component structure
- network-specialist: Plan sanitization flows

**Sequential Phase 2** (Implementation):
- engineer: Implement with TDD approach
- network-specialist: Add network-specific logic

**Parallel Phase 3** (Validation):
- engineer: Run tests (Jest + pytest)
- reviewer: Security + network compliance check

## Build Steps

### 1. Analysis & Planning
```bash
# Analyze requirements
architect: Design VS Code extension components
network-specialist: Plan IP sanitization architecture
```

### 2. Implementation (TDD)
```bash
# Write tests first
engineer: Create test files for new features
engineer: Implement TypeScript extension code
engineer: Implement FastAPI endpoints
```

### 3. Integration
```bash
# Connect components
engineer: Integrate VS Code UI with FastAPI backend
network-specialist: Add network parsing and sanitization
```

### 4. Validation
```bash
# Test everything
npm run test  # Jest tests
cd sanitization-server && python -m pytest  # Python tests
npm run lint  # TypeScript linting
```

### 5. Package
```bash
# Prepare for deployment
npm run compile
npm run package  # Create .vsix file
```

## Success Criteria
- All tests passing (Jest + pytest)
- Extension packages successfully
- Sanitization server starts and passes health checks
- Network features work with test configurations
- Security review passes