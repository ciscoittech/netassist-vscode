# NetAssist Project Structure

## Directory Layout
```
vscode-extension/
├── .claude/                    # Agent system (auto-loaded)
│   ├── agent-launcher.md      # Agent routing and selection
│   ├── settings.json          # Project configuration
│   └── commands/              # User workflows
│       ├── build.md          # TDD development cycle
│       ├── test.md           # Comprehensive testing
│       ├── debug.md          # Network-specific debugging
│       └── deploy.md         # Package and deployment
├── .claude-library/           # Agent library (on-demand)
│   ├── REGISTRY.json         # Agent registry and configuration
│   ├── agents/               # Specialized agents
│   │   ├── core/            # Core development agents
│   │   └── specialists/     # Network-specific agents
│   └── contexts/            # Project knowledge base
├── src/                      # VS Code extension source
│   ├── extension.ts         # Main extension entry point
│   ├── core/               # Core extension logic
│   └── providers/          # Service providers
├── sanitization-server/     # FastAPI backend
│   ├── main.py            # FastAPI application
│   ├── requirements.txt   # Python dependencies
│   ├── Dockerfile        # Container configuration
│   └── test_*.py         # Python test suite
└── package.json           # Extension manifest and dependencies
```

## Key Files

### VS Code Extension
- `package.json` - Extension manifest, commands, configuration
- `src/extension.ts` - Main extension activation and command handling
- `src/core/NetworkModeManager.ts` - Network mode switching logic
- `src/providers/SanitizationProvider.ts` - FastAPI communication

### FastAPI Backend
- `main.py` - FastAPI application with sanitization endpoints
- `requirements.txt` - Python dependencies (FastAPI, Pydantic, etc.)
- `simple_test.py` - Sanitization validation tests
- `docker-compose.yml` - Local development environment

## Development Patterns

### Extension Architecture
- Command-driven interface with VS Code command palette integration
- WebView-based chat interface for network assistance
- Provider pattern for backend service communication
- Configuration-driven network mode switching

### Backend Architecture
- RESTful API design with FastAPI and Pydantic validation
- Session-based sanitization with secure data handling
- Async processing for better performance
- Docker containerization for consistent deployment

### Network Specialization
- IP address and network range sanitization
- Configuration format detection and parsing
- pyATS integration for network testing
- Multi-vendor network device support

## Technology Choices

### Frontend (VS Code Extension)
- **TypeScript** - Type safety and VS Code API integration
- **VS Code Extension API** - Native IDE integration
- **WebView** - Rich UI components for chat interface

### Backend (Sanitization Server)
- **Python** - Network automation ecosystem compatibility
- **FastAPI** - Modern async web framework
- **Pydantic** - Data validation and serialization
- **Docker** - Containerized deployment

### Network Engineering
- **pyATS** - Cisco network testing framework
- **Network Config Parsing** - Multi-vendor support
- **IP Sanitization** - Secure data processing
- **Compliance Logging** - Enterprise audit requirements