# Contributing to NetAssist

We welcome contributions to NetAssist! This document outlines how to contribute to the project.

## 🚀 Quick Start

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/yourusername/netassist-vscode.git`
3. **Install** dependencies: `npm install`
4. **Setup** sanitization server: `cd sanitization-server && pip install -r requirements.txt`
5. **Run** tests: `npm test`

## 🏗️ Development Setup

### Prerequisites

- Node.js 18+
- Python 3.8+
- VS Code with Extension Development Pack

### Local Development

```bash
# Install extension dependencies
npm install

# Setup sanitization server
cd sanitization-server
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run tests
python simple_test.py
cd ..
npm test

# Start development server
./start.sh

# Open in VS Code and press F5 to launch Extension Development Host
```

## 🔒 Security Guidelines

### NEVER Commit:
- API keys or tokens
- Real network configurations with production IPs
- User data or credentials
- Sanitization mappings with real values

### Always:
- Use the sanitization server for any network data
- Test security features thoroughly
- Follow least privilege principles
- Document security implications

## 📋 Contribution Types

### 🐛 Bug Reports

Use the bug report template:

```markdown
**Bug Description**
Clear description of the bug

**Steps to Reproduce**
1. Step one
2. Step two
3. Step three

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g., Windows 10, macOS 12]
- VS Code: [e.g., 1.93.0]
- NetAssist: [e.g., 1.0.0]
- Sanitization Server: [Running/Not Running]
```

### ✨ Feature Requests

Use the feature request template:

```markdown
**Feature Description**
Clear description of the proposed feature

**Use Case**
Why is this feature needed?

**Proposed Solution**
How should this work?

**Network Engineering Context**
How does this fit into network workflows?

**Security Considerations**
Any security implications?
```

### 🔧 Code Contributions

#### Branch Naming
- `feature/vlan-sanitization`
- `fix/bgp-parsing-bug`
- `docs/api-documentation`
- `security/credential-detection`

#### Commit Messages
Follow conventional commits:

```bash
feat: add OSPF configuration templates
fix: resolve IP restoration bug in complex configs
docs: update security guidelines
test: add sanitization edge case tests
security: improve credential detection patterns
```

#### Pull Request Process

1. **Create branch** from `main`
2. **Implement** changes with tests
3. **Update** documentation if needed
4. **Run** all tests: `npm test && cd sanitization-server && python simple_test.py`
5. **Submit** PR with clear description

#### Code Review Checklist

- [ ] All tests pass
- [ ] Security tests pass
- [ ] No sensitive data in commits
- [ ] TypeScript compiles without errors
- [ ] Python code follows PEP 8
- [ ] Documentation updated
- [ ] Sanitization functionality tested

## 🧪 Testing

### Extension Tests
```bash
npm test
```

### Sanitization Server Tests
```bash
cd sanitization-server
python simple_test.py
python -m pytest test_sanitizer.py -v
```

### Security Tests
```bash
cd sanitization-server
python security_test.py
```

### Manual Testing Checklist

- [ ] Extension loads in VS Code
- [ ] Sanitization server starts
- [ ] All modes work (Config, Troubleshoot, Validate, Document)
- [ ] IP sanitization works correctly
- [ ] No real IPs leak to AI services
- [ ] Session management works
- [ ] Error handling graceful

## 📚 Documentation

### Code Documentation
- Use JSDoc for TypeScript
- Use docstrings for Python
- Comment complex algorithms
- Explain security decisions

### User Documentation
- Update README.md for user-facing changes
- Update DEVELOPMENT.md for developer changes
- Create examples for new features
- Update API documentation

## 🎯 Areas for Contribution

### High Priority
- **Multi-vendor support**: Juniper, Arista, F5 configuration parsing
- **Advanced sanitization**: MAC addresses, AS numbers, certificate data
- **Performance optimization**: Faster sanitization, reduced memory usage
- **Error handling**: Better error messages, recovery mechanisms

### Medium Priority
- **UI/UX improvements**: Better chat interface, mode switching
- **Testing**: More comprehensive test coverage
- **Documentation**: More examples, tutorials
- **Integrations**: pyATS, Ansible, Terraform

### Community Welcome
- **Language support**: Syntax highlighting for more vendors
- **Templates**: Common configuration templates
- **Examples**: Real-world use cases
- **Translations**: Internationalization support

## 🛡️ Security Reporting

### Reporting Security Issues

**DO NOT** create public GitHub issues for security vulnerabilities.

Instead:
1. Email: security@netassist.dev
2. Include: Detailed description, steps to reproduce, impact assessment
3. We'll respond within 24 hours
4. We'll work with you on responsible disclosure

### Security Scope
- IP/credential sanitization bypasses
- AI service data leakage
- Session hijacking vulnerabilities
- Code injection through configuration parsing
- Authentication/authorization issues

## 📄 License

By contributing to NetAssist, you agree that your contributions will be licensed under the MIT License.

## 🤝 Code of Conduct

### Our Standards

- **Respectful**: Treat everyone with respect
- **Inclusive**: Welcome diverse perspectives
- **Collaborative**: Work together constructively
- **Professional**: Maintain professional standards
- **Security-focused**: Prioritize user security and privacy

### Unacceptable Behavior

- Harassment of any kind
- Discriminatory language or actions
- Sharing others' private information
- Malicious security testing without permission
- Spam or off-topic discussions

### Enforcement

Report code of conduct violations to: conduct@netassist.dev

## 🎉 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Invited to contributor Discord
- Eligible for contributor rewards

## 📞 Getting Help

- **Discord**: [NetAssist Community](https://discord.gg/netassist)
- **Discussions**: [GitHub Discussions](https://github.com/netassist/netassist-vscode/discussions)
- **Issues**: [GitHub Issues](https://github.com/netassist/netassist-vscode/issues)
- **Email**: help@netassist.dev

---

Thank you for contributing to NetAssist! 🚀