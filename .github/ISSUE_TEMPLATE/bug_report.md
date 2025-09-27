---
name: Bug report
about: Create a report to help us improve NetAssist
title: '[BUG] '
labels: 'bug'
assignees: ''
---

## 🐛 Bug Description
A clear and concise description of what the bug is.

## 📋 Steps to Reproduce
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

## ✅ Expected Behavior
A clear and concise description of what you expected to happen.

## ❌ Actual Behavior
A clear and concise description of what actually happened.

## 🖼️ Screenshots
If applicable, add screenshots to help explain your problem.

## 🔧 Environment
- **OS**: [e.g., Windows 10, macOS 12, Ubuntu 20.04]
- **VS Code Version**: [e.g., 1.93.0]
- **NetAssist Version**: [e.g., 1.0.0]
- **Sanitization Server**: [Running/Not Running/Error]
- **AI Provider**: [e.g., OpenRouter, Claude, OpenAI]

## 🔒 Security Context
- [ ] This bug involves network configuration data
- [ ] This bug affects IP sanitization
- [ ] This bug could expose sensitive information
- [ ] This bug affects authentication/authorization

## 📝 Additional Context
Add any other context about the problem here.

## 🧪 Sanitization Server Status
If relevant, please include:
```bash
curl http://localhost:8000/api/health
```

## 📋 Logs
If applicable, please include relevant logs (with sensitive data removed):

**Extension Logs** (VS Code → Help → Toggle Developer Tools → Console):
```
[Paste logs here]
```

**Sanitization Server Logs**:
```
[Paste logs here]
```

## ✅ Checklist
- [ ] I have searched for existing issues
- [ ] I have removed any sensitive network information
- [ ] I have included all relevant environment details
- [ ] I can reproduce this bug consistently