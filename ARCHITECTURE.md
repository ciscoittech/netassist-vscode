# NetAssist VS Code Extension Architecture

## Overview

Building on proven patterns from Cline and Roo Coder, NetAssist provides network engineers with AI assistance while maintaining security through IP/credential sanitization.

## Core Architecture

```
┌─────────────────────────────────────┐
│           VS Code Extension         │
│  ┌─────────────────────────────────┐ │
│  │      Network Assistant UI       │ │
│  │   (Chat, Modes, File Diffs)     │ │
│  └─────────────────────────────────┘ │
│  ┌─────────────────────────────────┐ │
│  │     Network Mode Manager        │ │
│  │ (Config|Troubleshoot|Validate)  │ │
│  └─────────────────────────────────┘ │
│  ┌─────────────────────────────────┐ │
│  │    Sanitization Client          │ │
│  │  (Pre/Post AI processing)       │ │
│  └─────────────────────────────────┘ │
└─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────┐
│      FastAPI Sanitization Server   │
│  ┌─────────────────────────────────┐ │
│  │     IP/Credential Detector      │ │
│  │   (Regex + ML + Context)        │ │
│  └─────────────────────────────────┘ │
│  ┌─────────────────────────────────┐ │
│  │    Bidirectional Mapping        │ │
│  │  (Real ↔ Fake IP Storage)       │ │
│  └─────────────────────────────────┘ │
│  ┌─────────────────────────────────┐ │
│  │      Encryption Layer           │ │
│  │   (Local encrypted cache)       │ │
│  └─────────────────────────────────┘ │
└─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────┐
│         AI Model Provider           │
│    (Claude, GPT-4, Local LLM)       │
└─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────┐
│       Network Tool Integration      │
│     (pyATS, Cisco Docs, etc.)       │
└─────────────────────────────────────┘
```

## Extension Structure (Based on Cline)

```typescript
netassist/
├── src/
│   ├── extension.ts                 // Main extension entry point
│   ├── providers/
│   │   ├── NetworkAssistantProvider.ts  // Main chat provider
│   │   ├── SanitizationProvider.ts      // IP sanitization client
│   │   └── PyATSProvider.ts             // pyATS integration
│   ├── modes/
│   │   ├── ConfigMode.ts            // Network configuration mode
│   │   ├── TroubleshootMode.ts      // Troubleshooting mode
│   │   ├── ValidateMode.ts          // Validation/testing mode
│   │   └── DocumentMode.ts          // Documentation mode
│   ├── webview/
│   │   ├── NetAssistantPanel.tsx    // Main UI panel
│   │   ├── ChatInterface.tsx        // Chat component
│   │   └── ModeSelector.tsx         // Mode switching UI
│   ├── utils/
│   │   ├── networkDetection.ts      // Network entity detection
│   │   ├── configParser.ts          // Config file parsing
│   │   └── sanitizationCache.ts     // Local mapping cache
│   └── types/
│       ├── NetworkEntity.ts         // Type definitions
│       └── SanitizationMapping.ts   // Mapping types
├── package.json                     // Extension manifest
├── webpack.config.js               // Build configuration
└── sanitization-server/            // FastAPI server
    ├── main.py                     // Server entry point
    ├── sanitizer/
    │   ├── ip_detector.py          // IP detection logic
    │   ├── credential_detector.py  // Credential detection
    │   └── mapping_manager.py      // Bidirectional mapping
    ├── models/
    │   ├── network_entity.py       // Data models
    │   └── sanitization_session.py // Session management
    └── requirements.txt            // Python dependencies
```

## Key Components

### 1. Network Mode Manager (Core Innovation)

```typescript
class NetworkModeManager {
  private modes = {
    config: new ConfigMode(),
    troubleshoot: new TroubleshootMode(),
    validate: new ValidateMode(),
    document: new DocumentMode()
  };

  async processRequest(mode: string, request: string): Promise<string> {
    // 1. Sanitize input
    const sanitized = await this.sanitizer.sanitize(request);

    // 2. Route to appropriate mode
    const response = await this.modes[mode].process(sanitized);

    // 3. Restore real values
    return await this.sanitizer.restore(response);
  }
}
```

### 2. Sanitization Client (Secret Sauce)

```typescript
class SanitizationClient {
  private serverUrl = 'http://localhost:8000';

  async sanitize(text: string): Promise<SanitizedText> {
    const response = await fetch(`${this.serverUrl}/api/sanitize`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });

    return response.json();
  }

  async restore(text: string, mappingId: string): Promise<string> {
    const response = await fetch(`${this.serverUrl}/api/restore`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, mapping_id: mappingId })
    });

    return (await response.json()).restored_text;
  }
}
```

### 3. Network-Specific Modes

#### Configuration Mode
```typescript
class ConfigMode implements NetworkMode {
  private templates = new ConfigTemplateManager();

  async process(sanitizedRequest: string): Promise<string> {
    // Detect config type (VLAN, BGP, OSPF, etc.)
    const configType = this.detectConfigType(sanitizedRequest);

    // Load appropriate template
    const template = this.templates.get(configType);

    // Generate AI prompt with network context
    const prompt = this.buildNetworkPrompt(sanitizedRequest, template);

    // Get AI response
    return await this.aiProvider.complete(prompt);
  }
}
```

#### Troubleshooting Mode
```typescript
class TroubleshootMode implements NetworkMode {
  private docLoader = new CiscoDocLoader();

  async process(sanitizedRequest: string): Promise<string> {
    // Analyze symptoms
    const symptoms = this.analyzeSymptoms(sanitizedRequest);

    // Load relevant documentation sections
    const docs = await this.docLoader.loadRelevantSections(symptoms);

    // Build troubleshooting context
    const context = this.buildTroubleshootingContext(symptoms, docs);

    // Generate AI response with troubleshooting focus
    return await this.aiProvider.complete(context + sanitizedRequest);
  }
}
```

### 4. FastAPI Sanitization Server

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import re
from typing import Dict, List

app = FastAPI()

class IPSanitizer:
    def __init__(self):
        self.ip_patterns = [
            r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',  # IPv4
            r'\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b',  # IPv6
            r'\b(?:192\.168|10\.|172\.(?:1[6-9]|2[0-9]|3[0-1]))\.[0-9]{1,3}\.[0-9]{1,3}\b'  # Private IPs
        ]
        self.mappings: Dict[str, Dict[str, str]] = {}

    def sanitize(self, text: str, session_id: str) -> tuple[str, Dict[str, str]]:
        mapping = {}
        sanitized = text

        for pattern in self.ip_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if match not in mapping:
                    # Generate consistent fake IP
                    fake_ip = self.generate_fake_ip(match)
                    mapping[match] = fake_ip

                sanitized = sanitized.replace(match, mapping[match])

        # Store mapping for restoration
        self.mappings[session_id] = mapping
        return sanitized, mapping

    def restore(self, text: str, session_id: str) -> str:
        if session_id not in self.mappings:
            return text

        restored = text
        for real_ip, fake_ip in self.mappings[session_id].items():
            restored = restored.replace(fake_ip, real_ip)

        return restored
```

## Integration Points

### 1. pyATS Integration
```typescript
class PyATSProvider {
  async generateHealthCheck(devices: string[]): Promise<string> {
    const script = `
from pyats.topology import loader
from pyats import aetest

class NetworkHealthCheck(aetest.Testcase):
    @aetest.test
    def test_device_reachability(self, testbed):
        for device_name in ${JSON.stringify(devices)}:
            device = testbed.devices[device_name]
            device.connect()
            output = device.execute('show version')
            assert 'uptime' in output.lower()
            device.disconnect()
`;
    return script;
  }
}
```

### 2. Cisco Documentation Loader
```typescript
class CiscoDocLoader {
  async loadRelevantSections(symptoms: string[]): Promise<string> {
    // Use existing cisco-doc-fetcher logic
    const relevantSections = this.identifyRelevantSections(symptoms);

    // Load only 5-10KB of targeted content
    return await this.fetchSections(relevantSections);
  }
}
```

## Security Architecture

### 1. Local Processing
- All sanitization happens locally
- No sensitive data sent to cloud APIs
- Encrypted local cache for mappings

### 2. Session Management
```typescript
class SecureSessionManager {
  private sessions = new Map<string, SanitizationSession>();

  createSession(): string {
    const sessionId = this.generateSecureId();
    this.sessions.set(sessionId, new SanitizationSession());
    return sessionId;
  }

  expireSession(sessionId: string): void {
    // Clear all mappings and cache
    this.sessions.delete(sessionId);
  }
}
```

### 3. Audit Trail
```typescript
interface SanitizationAudit {
  timestamp: Date;
  originalHash: string;  // Hash of original text (no actual content)
  sanitizedHash: string; // Hash of sanitized text
  mappingCount: number;  // Number of entities sanitized
  success: boolean;
}
```

## Development Workflow

### 1. Fork Cline Base
- Start with Cline's proven chat interface
- Replace generic coding modes with network modes
- Add sanitization layer before AI calls

### 2. Incremental Development
- Week 1: Basic extension with sanitization
- Week 2: Network modes and pyATS
- Week 3: Documentation integration
- Week 4: Testing and polish

### 3. Packaging Strategy
- VS Code marketplace publication
- Docker container for sanitization server
- Documentation and setup guides

This architecture leverages proven patterns while adding network-specific value through intelligent sanitization and domain expertise.