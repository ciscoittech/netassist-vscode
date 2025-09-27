# NetAssist Development Guide

This guide covers development setup, architecture, and contribution guidelines for the NetAssist VS Code extension.

## 🏗️ Architecture Overview

NetAssist follows a multi-component architecture designed for security and modularity:

```
┌─────────────────────────────────────┐
│           VS Code Extension         │
│  ┌─────────────────────────────────┐ │
│  │      Network Assistant UI       │ │ ← React/TypeScript
│  │   (Chat, Modes, File Diffs)     │ │
│  └─────────────────────────────────┘ │
│  ┌─────────────────────────────────┐ │
│  │     Network Mode Manager        │ │ ← TypeScript
│  │ (Config|Troubleshoot|Validate)  │ │
│  └─────────────────────────────────┘ │
│  ┌─────────────────────────────────┐ │
│  │    Sanitization Client          │ │ ← TypeScript
│  │  (Pre/Post AI processing)       │ │
│  └─────────────────────────────────┘ │
└─────────────────────────────────────┘
                    │ HTTP/JSON
                    ▼
┌─────────────────────────────────────┐
│      FastAPI Sanitization Server   │ ← Python
│  ┌─────────────────────────────────┐ │
│  │     IP/Credential Detector      │ │ ← RegEx + ML
│  │   (Regex + ML + Context)        │ │
│  └─────────────────────────────────┘ │
│  ┌─────────────────────────────────┐ │
│  │    Bidirectional Mapping        │ │ ← In-memory/Redis
│  │  (Real ↔ Fake IP Storage)       │ │
│  └─────────────────────────────────┘ │
└─────────────────────────────────────┘
                    │ API calls
                    ▼
┌─────────────────────────────────────┐
│         AI Model Provider           │ ← External APIs
│    (Claude, GPT-4, Local LLM)       │
└─────────────────────────────────────┘
```

## 🛠️ Development Setup

### Prerequisites

- **Node.js 18+** for VS Code extension development
- **Python 3.8+** for sanitization server
- **VS Code** with extension development pack
- **Docker** (optional, for containerized development)

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/netassist/vscode-extension
cd vscode-extension

# Install extension dependencies
npm install

# Setup sanitization server
cd sanitization-server
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run tests
python simple_test.py

# Start development
cd ..
./start.sh
```

### VS Code Extension Development

```bash
# Install dependencies
npm install

# Compile TypeScript
npm run compile

# Watch for changes during development
npm run watch

# Open extension host for testing
# Press F5 in VS Code to launch Extension Development Host
```

### Project Structure

```
vscode-extension/
├── src/                          # Extension source code
│   ├── extension.ts             # Main extension entry point
│   ├── providers/               # Core service providers
│   │   ├── NetAssistantProvider.ts    # Main chat provider
│   │   ├── SanitizationProvider.ts    # IP sanitization client
│   │   └── PyATSProvider.ts           # pyATS integration
│   ├── modes/                   # Network-specific modes
│   │   ├── ConfigMode.ts        # Configuration assistance
│   │   ├── TroubleshootMode.ts  # Issue diagnosis
│   │   ├── ValidateMode.ts      # Config validation
│   │   └── DocumentMode.ts      # Documentation lookup
│   ├── core/                    # Core functionality
│   │   ├── NetworkModeManager.ts     # Mode routing
│   │   └── ConfigurationManager.ts   # Settings management
│   └── webview/                 # React UI components
│       ├── NetAssistantPanel.tsx     # Main panel
│       ├── ChatInterface.tsx         # Chat component
│       └── ModeSelector.tsx          # Mode switching
├── sanitization-server/         # Python sanitization service
│   ├── main.py                  # FastAPI server
│   ├── simple_test.py          # Core functionality tests
│   ├── requirements.txt        # Python dependencies
│   └── Dockerfile              # Container configuration
├── package.json                # Extension manifest
├── tsconfig.json              # TypeScript configuration
└── webpack.config.js          # Build configuration
```

## 🔧 Core Components

### 1. Sanitization Provider

The heart of NetAssist's security model:

```typescript
class SanitizationProvider {
  async sanitize(text: string): Promise<SanitizationResponse> {
    // 1. Send text to sanitization server
    // 2. Receive sanitized text + mapping ID
    // 3. Store session for later restoration
  }

  async restore(text: string, sessionId: string): Promise<string> {
    // 1. Send AI response to server
    // 2. Restore original values using stored mapping
    // 3. Return text with real network values
  }
}
```

### 2. Network Mode Manager

Routes requests to appropriate domain experts:

```typescript
class NetworkModeManager {
  private modes = {
    config: new ConfigMode(),
    troubleshoot: new TroubleshootMode(),
    validate: new ValidateMode(),
    document: new DocumentMode()
  };

  async processRequest(request: string): Promise<string> {
    const mode = this.modes[this.currentMode];
    return await mode.processRequest(request, this.context);
  }
}
```

### 3. Mode Implementations

Each mode provides specialized network assistance:

```typescript
interface NetworkModeHandler {
  processRequest(request: string, context?: any): Promise<string>;
  getSystemPrompt(): string;
  getSuggestedActions(): string[];
}
```

## 🧪 Testing Strategy

### Unit Tests

```bash
# Run extension tests
npm test

# Run sanitization server tests
cd sanitization-server
python simple_test.py
```

### Integration Tests

```bash
# Test full sanitization cycle
cd sanitization-server
pytest test_sanitizer.py -v
```

### Security Tests

```bash
# Verify no data leakage
python security_test.py
```

## 🔒 Security Considerations

### Data Flow Security

1. **Input Sanitization**: All network configurations are sanitized before AI processing
2. **Session Isolation**: Each sanitization session uses unique, time-limited mappings
3. **No Data Persistence**: Original network data is never stored permanently
4. **Audit Logging**: All operations are logged for compliance (hashed content only)

### Code Security Guidelines

```typescript
// ✅ Good: Always sanitize before AI calls
const sanitized = await this.sanitizer.sanitize(userInput);
const aiResponse = await this.aiProvider.complete(sanitized.sanitized_text);
const restored = await this.sanitizer.restore(aiResponse, sanitized.session_id);

// ❌ Bad: Never send raw network data to AI
const aiResponse = await this.aiProvider.complete(userInput); // SECURITY VIOLATION
```

### Sanitization Rules

The sanitization server follows these rules:

- **IPv4 addresses**: 192.168.x.x → 10.255.x.x (preserving subnet structure)
- **Private IPs**: 10.x.x.x → 172.31.x.x (maintaining relationships)
- **Public IPs**: Any public → 203.0.113.x (RFC 5737 test range)
- **VLANs**: Increment from 100 (VLAN 50 → VLAN 100)
- **Hostnames**: Replace with device1, device2, etc.
- **AS Numbers**: Increment from 65000

## 🚀 Building and Deployment

### Development Build

```bash
npm run compile
```

### Production Build

```bash
npm run vscode:prepublish
```

### Extension Packaging

```bash
# Install VSCE (VS Code Extension CLI)
npm install -g vsce

# Package extension
vsce package

# Publish to marketplace (requires publisher account)
vsce publish
```

### Docker Deployment

```bash
# Build sanitization server image
cd sanitization-server
docker build -t netassist-sanitizer .

# Deploy with docker-compose
docker-compose up -d
```

## 📋 Contributing Guidelines

### Code Style

- **TypeScript**: Use strict type checking
- **Python**: Follow PEP 8 with 100 character line limit
- **Comments**: Focus on "why", not "what"
- **Naming**: Use descriptive names (sanitizeNetworkConfig, not sanitize)

### Commit Messages

Follow conventional commits:

```bash
feat: add VLAN sanitization support
fix: resolve IP restoration bug in complex configs
docs: update security guidelines
test: add sanitization edge case tests
```

### Pull Request Process

1. **Fork** the repository
2. **Create** feature branch (`feature/vlan-sanitization`)
3. **Implement** changes with tests
4. **Verify** all tests pass
5. **Submit** pull request with clear description

### Required Checks

- ✅ All unit tests pass
- ✅ Security tests pass
- ✅ TypeScript compiles without errors
- ✅ Python code passes linting
- ✅ No sensitive data in commit history

## 🐛 Debugging

### Extension Debugging

1. Open VS Code
2. Press `F5` to launch Extension Development Host
3. Open Developer Tools (`Help > Toggle Developer Tools`)
4. Set breakpoints in TypeScript source

### Sanitization Server Debugging

```bash
# Enable debug logging
cd sanitization-server
LOG_LEVEL=debug python main.py

# Use debugger
python -m pdb main.py
```

### Common Issues

**Extension Not Loading**
```bash
# Check extension host logs
# VS Code → Help → Toggle Developer Tools → Console
```

**Sanitization Server Connection**
```bash
# Verify server health
curl http://localhost:8000/api/health

# Check firewall/port conflicts
lsof -i :8000
```

**TypeScript Compilation Errors**
```bash
# Clean build
npm run clean
npm run compile
```

## 📊 Performance Monitoring

### Metrics to Track

- **Sanitization latency**: <100ms for typical configs
- **Memory usage**: <50MB for sanitization server
- **Success rate**: >99.9% sanitization accuracy
- **Session cleanup**: Automatic cleanup after 24 hours

### Monitoring Commands

```bash
# Check sanitization server performance
curl http://localhost:8000/api/health

# Monitor memory usage
ps aux | grep python

# Check active sessions
curl http://localhost:8000/api/sessions/stats
```

## 🔮 Future Development

### Planned Features

- **Multi-vendor support**: Juniper, Arista, F5 configurations
- **Advanced ML detection**: Improved entity detection accuracy
- **Team collaboration**: Shared sanitization sessions
- **Custom rules**: User-defined sanitization patterns

### Architecture Evolution

- **Microservices**: Split sanitization into specialized services
- **Caching layer**: Redis for session management
- **Load balancing**: Multiple sanitization server instances
- **Monitoring**: Prometheus metrics and Grafana dashboards

---

Ready to contribute? Start with a simple feature and gradually work your way up to more complex components. The codebase is designed to be modular and testable.

**Happy coding!** 🚀