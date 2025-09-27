# NetAssist Test Command

## Purpose
Comprehensive testing for VS Code extension and FastAPI sanitization server

## Agents Required
- **engineer**: Execute and analyze test results
- **network-specialist**: Validate network-specific test scenarios

## Test Strategy

### VS Code Extension Tests (Jest)
```bash
npm run test
```
**Test Coverage:**
- Extension activation/deactivation
- Command registration and execution
- Chat interface functionality
- Configuration management
- Network mode switching

### FastAPI Backend Tests (pytest)
```bash
cd sanitization-server
python -m pytest -v
```
**Test Coverage:**
- IP sanitization accuracy
- API endpoint functionality
- Session management
- Error handling
- Performance benchmarks

### Integration Tests
```bash
# End-to-end workflow tests
engineer: Test VS Code → FastAPI communication
network-specialist: Test complete sanitization workflow
```

## Test Scenarios

### Network Sanitization Tests
- IPv4/IPv6 address replacement
- VLAN ID sanitization
- Hostname obfuscation
- MAC address anonymization
- Configuration structure preservation

### VS Code Extension Tests
- Panel rendering and UI interactions
- Command palette integration
- Settings persistence
- File detection and processing

### Error Handling Tests
- Sanitization server unavailable
- Invalid network configurations
- API timeout scenarios
- Malformed user inputs

## Success Criteria
- Jest tests: >90% coverage
- pytest tests: >85% coverage
- All integration tests pass
- Performance benchmarks met (<200ms sanitization)
- No security test failures