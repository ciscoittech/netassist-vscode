# NetAssist - AI Network Engineer VS Code Extension

**🚀 AI-powered network automation with secure IP sanitization**

NetAssist is the first VS Code extension specifically designed for network engineers, providing AI assistance while keeping your sensitive network data secure through intelligent IP/credential sanitization.

## 🎯 Key Features

- **🔒 Secure IP Sanitization**: Your real IPs never reach AI services
- **🔧 Network-Specific Modes**: Config, Troubleshoot, Validate, Document
- **⚡ pyATS Integration**: Generate network tests and automation
- **📚 Smart Documentation**: Load relevant Cisco docs on-demand
- **🎨 Cisco Syntax Highlighting**: Enhanced network config editing

## 🔥 The Problem We Solve

Network engineers need AI help but can't expose production IPs, VLANs, hostnames, and credentials to cloud AI services. NetAssist solves this with a local sanitization layer that:

1. **Sanitizes** your network configs (192.168.1.1 → 10.255.1.1)
2. **Processes** sanitized data with AI safely
3. **Restores** real values in AI responses
4. **Audits** all operations for compliance

## 🚀 Quick Start

### Prerequisites

- VS Code 1.93+
- Python 3.8+ (for sanitization server)
- Docker (optional, for containerized deployment)

### Installation

1. **Install the extension** (coming to VS Code marketplace)
2. **Start sanitization server**:
   ```bash
   cd sanitization-server
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python main.py
   ```
3. **Configure your AI provider** in VS Code settings

### First Steps

1. Open VS Code with a network configuration file
2. Press `Ctrl+Shift+P` → "NetAssist: Open Chat"
3. Ask: "Help me configure a VLAN"
4. Watch as NetAssist sanitizes IPs and provides secure assistance!

## 🔧 Usage Examples

### Configuration Mode
```
User: Create a VLAN 100 configuration for 192.168.1.0/24 network

NetAssist:
- Sanitizes: 192.168.1.0/24 → 10.255.1.0/24
- AI generates config with sanitized IPs
- Restores real IPs: 10.255.1.0/24 → 192.168.1.0/24
```

### Troubleshooting Mode
```
User: BGP neighbor 172.16.1.1 is down

NetAssist:
- Sanitizes: 172.16.1.1 → 203.0.113.1
- Loads relevant BGP troubleshooting docs
- Provides step-by-step diagnosis with real IP restored
```

### pyATS Integration
```
User: Generate a health check for my routers

NetAssist:
- Creates pyATS test script
- Sanitizes device IPs in testbed
- Generates executable test with real values
```

## 🏗️ Architecture

```
VS Code Extension
    ↓ (sanitized data)
FastAPI Sanitization Server ← Your Secret Sauce
    ↓ (safe for AI)
AI Provider (Claude/GPT-4)
    ↓ (AI response)
pyATS/Network Tools
```

### Security Model

1. **Local Processing**: All sanitization happens on your machine
2. **No Data Leakage**: Real IPs never sent to cloud AI
3. **Audit Trail**: Complete log of all sanitization operations
4. **Session Isolation**: Each sanitization session is isolated

## 📋 Configuration

### VS Code Settings

```json
{
  "netassist.sanitizationServer": "http://localhost:8000",
  "netassist.aiProvider": "anthropic",
  "netassist.defaultMode": "config",
  "netassist.autoSanitize": true,
  "netassist.sanitizationLevel": "balanced"
}
```

### AI Provider Setup

#### Anthropic Claude
```json
{
  "netassist.aiProvider": "anthropic",
  "netassist.anthropic.apiKey": "sk-ant-..."
}
```

#### OpenAI
```json
{
  "netassist.aiProvider": "openai",
  "netassist.openai.apiKey": "sk-..."
}
```

## 🔄 Available Commands

| Command | Description | Shortcut |
|---------|-------------|----------|
| `NetAssist: Open Chat` | Open AI assistant panel | `Ctrl+Shift+A` |
| `NetAssist: Switch Mode` | Change assistance mode | `Ctrl+Shift+M` |
| `NetAssist: Sanitize Selection` | Sanitize selected text | `Ctrl+Shift+S` |
| `NetAssist: Generate pyATS` | Create pyATS test script | `Ctrl+Shift+T` |
| `NetAssist: Load Cisco Docs` | Load documentation | `Ctrl+Shift+D` |

## 🧪 Testing the Sanitization

The sanitization server includes comprehensive tests:

```bash
cd sanitization-server
python simple_test.py
```

**Expected Output:**
```
🎯 Test Summary
Tests passed: 3/3
🎉 All tests passed! Sanitization system is working correctly.
✅ Ready for VS Code extension integration
```

## 🐳 Docker Deployment

For consistent deployment across teams:

```bash
cd sanitization-server
docker-compose up -d
```

This starts the sanitization server on `http://localhost:8000` with health checks and automatic restarts.

## 📊 Compliance & Auditing

NetAssist maintains detailed audit logs for compliance:

```bash
# View sanitization audit log
Ctrl+Shift+P → "NetAssist: Export Audit Log"
```

**Audit Log Contents:**
- Timestamp of each operation
- Number of entities sanitized
- Confidence scores
- Session IDs
- Hashed content (no actual data)

## 🛡️ Security Features

### What Gets Sanitized

- **IPv4/IPv6 addresses**: 192.168.1.1 → 10.255.1.1
- **Network ranges**: 10.0.0.0/8 → 172.31.0.0/16
- **VLAN IDs**: VLAN 100 → VLAN 200
- **Device hostnames**: CORE-SW-01 → device1
- **AS numbers**: BGP 65001 → BGP 65100
- **MAC addresses**: 00:1b:21:3a:4f:5e → 00:11:22:33:44:55

### What Stays the Same

- Configuration structure and syntax
- Command keywords (interface, vlan, bgp)
- Non-sensitive network concepts
- Error messages and logs structure

## 🚀 Roadmap

### v1.0 (Current)
- ✅ Basic IP/VLAN sanitization
- ✅ Four network modes
- ✅ pyATS integration
- ✅ Cisco documentation loader

### v1.1 (Next)
- 🔄 Multi-vendor support (Juniper, Arista)
- 🔄 Advanced credential detection
- 🔄 Team collaboration features
- 🔄 Custom sanitization rules

### v2.0 (Future)
- 🔄 Enterprise SSO integration
- 🔄 Advanced compliance reporting
- 🔄 Custom AI model support
- 🔄 Multi-project orchestration

## 💡 Pro Tips

1. **Use Config Mode** for building new configurations
2. **Switch to Troubleshoot Mode** when diagnosing issues
3. **Validate Mode** helps review configurations before deployment
4. **Document Mode** for quick Cisco documentation lookups
5. **Check audit logs** regularly for compliance verification

## 🤝 Contributing

We welcome contributions! Please see:

- [Architecture Guide](./ARCHITECTURE.md)
- [Development Setup](./DEVELOPMENT.md)
- [Security Guidelines](./SECURITY.md)

## 📄 License

MIT License - Use freely in your projects, commercial or otherwise.

## 🆘 Support

- **Documentation**: [GitHub Wiki](https://github.com/netassist/vscode-extension/wiki)
- **Issues**: [GitHub Issues](https://github.com/netassist/vscode-extension/issues)
- **Discussions**: [GitHub Discussions](https://github.com/netassist/vscode-extension/discussions)

---

## 🎉 Ready to Get Started?

```bash
# Quick setup
git clone https://github.com/netassist/vscode-extension
cd vscode-extension/sanitization-server
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python main.py

# Install VS Code extension
# Configure AI provider
# Start network engineering with AI assistance!
```

**Your network automation journey starts here.** 🚀

---

*Built with ❤️ for network engineers who value both innovation and security.*