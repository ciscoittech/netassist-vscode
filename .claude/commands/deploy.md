# NetAssist Deploy Command

## Purpose
Package and deploy VS Code extension with sanitization server for distribution

## Agents Required
- **architect**: Validate deployment architecture and dependencies
- **reviewer**: Security review and compliance validation

## Deployment Strategy

### Pre-Deployment Validation
```bash
# Ensure all components are ready
architect: Validate extension manifest and dependencies
reviewer: Security audit and compliance check
engineer: Final test suite execution
```

### Extension Packaging
```bash
# Build and package VS Code extension
npm run compile
npm run lint
npm run test
npm run package  # Creates .vsix file
```

### Sanitization Server Packaging
```bash
# Prepare FastAPI backend for distribution
cd sanitization-server
docker build -t netassist-sanitizer .
docker-compose build
```

## Deployment Targets

### VS Code Marketplace
```bash
# Publish to official marketplace
vsce publish
# Requires publisher account and marketplace approval
```

### GitHub Releases
```bash
# Create GitHub release with .vsix file
gh release create v1.0.0 ./netassist-1.0.0.vsix
# Include sanitization server Docker image
```

### Enterprise Distribution
```bash
# Package for internal enterprise deployment
# Include setup scripts and documentation
# Provide Docker Compose configuration
```

## Deployment Checklist

### Extension Validation
- [ ] Extension activates correctly in clean VS Code instance
- [ ] All commands registered and functional
- [ ] UI components render properly
- [ ] Configuration settings work as expected
- [ ] No console errors during normal operation

### Backend Validation
- [ ] FastAPI server starts and responds to health checks
- [ ] All API endpoints functional
- [ ] Docker image builds successfully
- [ ] Environment variables properly configured
- [ ] Performance benchmarks met

### Security Review
- [ ] No hardcoded credentials or sensitive data
- [ ] Proper input validation on all endpoints
- [ ] Secure communication between components
- [ ] Audit logging functional and complete
- [ ] Data sanitization tested and verified

### Documentation
- [ ] README.md updated with installation instructions
- [ ] Configuration guide complete
- [ ] Troubleshooting documentation available
- [ ] API documentation generated and accurate

## Distribution Assets

### Extension Package
- `netassist-1.0.0.vsix` - VS Code extension package
- Installation and configuration documentation
- License and terms of use

### Sanitization Server
- Docker image and Docker Compose configuration
- Python requirements and setup scripts
- Health check and monitoring endpoints

### Supporting Materials
- Setup and installation guides
- Network engineering usage examples
- Security and compliance documentation

## Success Criteria
- Extension packages without errors
- All deployment targets accessible
- Documentation complete and accurate
- Security review passes all requirements
- Performance benchmarks met in production environment