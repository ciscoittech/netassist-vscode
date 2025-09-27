# Product Requirements Document (PRD)
## NetAssist VS Code Extension

---

## 1. Problem Statement & Success Metrics (30 mins)

**Problem:** Network engineers across all domains (Linux networking, cloud infrastructure, security, VoIP, wireless, multi-vendor environments) need AI guidance for configuration, troubleshooting, and validation tasks, but current AI tools expose sensitive network data (IPs, credentials, topology) to cloud services, creating security risks that prevent enterprise adoption.

**Solution:** Fork proven agent platforms (Cline/Roo Coder) to create an AI workflow builder for network engineering - users get built-in network flows plus an AI assistant that helps them build custom workflows using Claude Agent Framework patterns, with FastAPI sanitization, pyATS tool calling, and Qwen models.

**Success Metrics:**
- **Revenue target:** 1,000 network engineers at $29/month within 6 months ($348K ARR)
- **Security KPI:** 100% sensitive data sanitization with 0% data leakage to cloud APIs
- **Technical performance:** <200ms sanitization latency, 95% network entity detection accuracy

**Target User:** Network Engineers across all specialties who work with configurations that need structured analysis - Linux admins with iptables rules, cloud engineers with AWS configs, security engineers with firewall rules, VoIP engineers with SIP configs, wireless engineers with controller configs, and traditional network engineers with router/switch configs.

---

## 2. User Stories with Acceptance Criteria (1 hour)

### Core User Flow
**Story:** "As a network engineer, I want to use built-in network workflows and build my own custom workflows with an AI assistant, while automatically protecting sensitive data through sanitization and pyATS parsing"

**Acceptance Criteria:**
- ✓ User opens VS Code with forked interface, can choose built-in flows (BGP troubleshooting, security audit) or "Build Custom Workflow"
- ✓ For built-in: User pastes BGP config, FastAPI sanitizes, agents call pyATS tools to parse config and diagnose issues
- ✓ For custom: AI Workflow Builder prompts "What do you want to analyze?" → "Packet captures for security threats" → AI generates workflow.md with agents + tool calls
- ✓ Custom workflow includes: packet-analyzer agent calling Wireshark container, security-auditor calling pyATS parsers, parallel execution patterns
- ✓ User launches custom workflow: "Run my packet security analysis" → agents execute with sanitized data → pyATS parses network data → tools run in Docker
- ✓ Results synthesized: "Found 3 suspicious connections in sanitized capture, pyATS validation shows protocol anomalies" with mapping restoration

---

## 3. Detailed Feature Specs (1-2 hours)

### Forked Agent Platform Customization
**Input:** Existing Cline/Roo Coder VS Code extension infrastructure
**Process:**
- Fork proven agent platform repository and preserve core chat interface, agent orchestration, and tool calling framework
- Replace default agents with network specialist agents from examples/ directory (network-troubleshooter.md, security-engineer.md, etc.)
- Integrate FastAPI sanitization server as pre-processing layer for all network configurations
- Configure Qwen model integration via OpenRouter API replacing original Claude/GPT model calls
**Output:** Network-specialized agent platform leveraging proven VS Code integration and workflow management
**Error Handling:** Platform compatibility issues → Maintain original agent framework APIs, Missing network agents → Graceful fallback to general troubleshooting
**Performance:** Inherit existing performance optimizations, add <200ms sanitization layer

### Dynamic Network Agent Library System
**Input:** User questions, detected configuration types, and workflow requirements
**Process:**
- Agent Launcher analyzes user intent and dynamically loads appropriate network specialist agents
- Route parallel agent execution using existing platform's multi-agent orchestration capabilities
- Each agent (as prompt) sent to Qwen models with specialized network engineering context and tool access
- Synthesize results from multiple agents into coherent recommendations and actionable insights
**Output:** Coordinated multi-agent network analysis with specialist expertise per domain
**Validation:** Agent selection accuracy, parallel execution success, result synthesis quality
**Side Effects:** Build library of successful agent combinations and workflow patterns for common network scenarios

### AI Workflow Builder Engine
**Input:** User requirements for custom workflows ("I want to analyze packet captures for security threats")
**Process:**
- AI assistant prompts user through workflow definition using Claude Agent Framework patterns
- Generate workflow.md files with agents, tool calls (pyATS parsers, Docker containers), and execution flow
- Validate workflow against framework best practices and tool availability
- Store custom workflows alongside built-in flows for future execution
**Output:** Executable workflow files that follow Claude Agent Framework patterns with pyATS integration
**Validation:** Workflow syntax validation, tool availability checks, agent compatibility verification
**Side Effects:** Build library of user-generated workflows for community sharing and reuse

### Network Tool Orchestration Layer
**Authentication/Access:** Leverage existing platform's tool calling framework extended with network-specific capabilities
**Business Logic:** Coordinate pyATS parsers, Docker containers (Wireshark, custom tools), validation services, and documentation lookup
**Data Flow:** Sanitized configs → Agent prompts + tool definitions → Qwen execution → Tool calling (pyATS, containers) → Result synthesis

---

## 4. Technical Constraints & Assumptions (20 mins)

**Budget:** Bootstrap by forking existing open-source platforms - $0 infrastructure cost, user provides OpenRouter API keys for Qwen models
**Performance:** Inherit existing agent platform performance + 10 concurrent multi-agent workflows, <200ms sanitization, <3s parallel agent execution
**Platform Support:** Fork Cline/Roo Coder VS Code extensions, maintain existing Node.js/TypeScript stack, add Python FastAPI sanitization layer
**Security:** All sensitive data processed locally via FastAPI, agents receive only sanitized data, leverage existing platform's session management
**Infrastructure:** Forked VS Code extension + FastAPI sanitization server (local/docker) + Qwen models via OpenRouter
**Scalability:** Leverage existing platform's architecture for single-user workflows, extend for team agent libraries and custom workflow sharing

---

## 5. UI Wireframes with Behavior (30 mins)

### Main Chat Interface (Embedded in VS Code)
- **Layout:** Right sidebar panel, 400px width, scrollable chat history with mode selector at top
- **Element States:** Mode buttons (Config|Troubleshoot|Validate|Design) highlight active mode, typing indicator during AI processing
- **Content Structure:** User messages (right-aligned), AI responses (left-aligned) with syntax highlighting for configs
- **Behavior:** File drag-drop auto-detects config type and switches to appropriate mode

### Inherited Chat Interface with Network Agents
- **Layout:** Leverage existing Cline/Roo Coder chat interface - left sidebar chat panel with message history and agent indicators
- **Interactive Elements:** Agent status badges show active specialists (🔧 troubleshooter, 🛡️ security-engineer, ⚙️ config-manager), typing indicators during parallel execution
- **Data Display:** Current active agents, sanitization status indicator, multi-agent progress with individual agent completion states
- **Navigation:** Seamless chat experience with agent specialization happening transparently, users chat naturally without mode switching

### Dynamic Agent Loading Panel
- **Loading States:** "Loading network specialists..." with agent selection reasoning, "Agents analyzing..." with parallel execution progress
- **Error States:** Agent loading failures with fallback options, sanitization warnings with manual review prompts, tool calling errors with alternative approaches
- **Empty States:** "What network challenge can I help with?" with suggested workflows: troubleshooting, security audit, configuration validation

---

## 6. API Contracts (30 mins)

### FastAPI Sanitization Layer (Pre-Agent Processing)
```
POST /api/sanitize
Request: {config_text: string, config_type: "auto"|"ios"|"nxos"|"asa"|"linux"|"cloud"}
Response: {sanitized_config: string, mapping_id: string, entities_replaced: Array<{type: string, count: number}>, confidence_score: number}
```

### Agent Launcher Integration (Forked Platform)
```
POST /internal/agent-launcher
Request: {user_question: string, sanitized_context: object, available_agents: Array<string>}
Response: {selected_agents: Array<{agent_id: string, agent_prompt: string}>, execution_strategy: "parallel"|"sequential", estimated_time: number}
```

### Qwen Model Integration (Replace Platform's AI Calls)
```
POST /api/qwen-agents
Request: {agents: Array<{prompt: string, tools: Array<string>}>, sanitized_data: object, user_context: object}
Response: {agent_results: Array<{agent_id: string, result: string, tool_calls: Array<object>}>, synthesis: string, mapping_restoration: object}
```

---

## 7. Core MVP Tests Only (30 mins)

**Critical Path Tests:**
```
- Fork compatibility: Verify forked Cline/Roo Coder maintains original functionality while adding network features
- FastAPI sanitization integration: Config paste → sanitization → agent processing without data leakage
- Dynamic agent loading: User question → agent launcher selects appropriate network specialists → parallel execution
- End-to-end multi-agent workflow: BGP issue → network-troubleshooter + config-manager → Qwen model execution → synthesis
```

**Essential Error Tests:**
```
- Platform integration failures → graceful fallback to single-agent mode with clear error messaging
- Sanitization service unavailable → offline mode with security warnings and manual review prompts
- Agent loading failures → fallback agent selection with alternative specialist recommendations
```

**Skip for MVP:**
- Load testing beyond 3 concurrent multi-agent workflows (inherit platform limits)
- Advanced agent orchestration patterns (focus on parallel execution initially)
- Complex tool calling chain optimizations
- Enterprise team sharing of custom agent libraries

---

## 8. Minimal Data Models (15 mins)

```
NetworkEntity: id, type (ip|password|hostname|community), original_value, sanitized_value, regex_pattern_used
SanitizationSession: session_id, created_at, expires_at, entity_mappings, encrypted_data
AgentExecution: execution_id, selected_agents, execution_strategy, start_time, completion_status, results
NetworkAgent: agent_id, agent_name, agent_prompt_template, supported_tools, trigger_keywords, specialization_domain
MultiAgentSession: session_id, user_context, active_agents, sanitized_data_refs, synthesis_results, chat_history
```

**Security Notes:**
- All original_value fields encrypted at rest with AES-256
- Session data auto-purged after 2 hours with complete mapping cleanup
- Agents receive only sanitized data, never original network values or credentials
- Leverage existing platform's security model while adding sanitization layer protection

---

## 9. Additional Technical Requirements (Missing from Standard Template)

### Platform Fork Integration Strategy
**Cline/Roo Coder Compatibility:** Maintain existing agent orchestration, chat interface, and tool calling framework while adding network specialization
**Network Agent Library:** Replace default agents with network specialists from examples/ directory (network-troubleshooter.md, security-engineer.md, etc.)
**Qwen Model Integration:** Replace original AI model calls with Qwen via OpenRouter while preserving agent execution patterns
**FastAPI Sanitization Layer:** Add pre-processing sanitization service that integrates seamlessly with existing platform workflows

### Multi-Agent Network Intelligence Framework
**Dynamic Agent Selection:** Agent launcher analyzes user intent and loads appropriate network specialists on-demand
**Parallel Execution Leverage:** Utilize existing platform's multi-agent orchestration for network specialist coordination
**Tool Calling Extension:** Add network-specific tools (pyATS parsers, validation services, documentation lookup) to existing framework
**Result Synthesis:** Coordinate multiple agent outputs into coherent network recommendations and actionable insights

### Enterprise Network Security and Compliance
**Sanitization-First Architecture:** All network data processed through FastAPI sanitization before any agent interaction
**Zero Data Leakage:** Agents and AI models receive only sanitized data, original network values never leave local environment
**Inherited Security Model:** Leverage existing platform's session management, error handling, and user authentication while adding network-specific protections
**Compliance Ready:** SOC2, ISO27001, and network security audit trails with comprehensive operation logging

---

**Total PRD Time: ~4.5 hours**
**Deliverable: Engineering has exactly what they need to fork Cline/Roo Coder, add FastAPI sanitization layer, replace agents with network specialists, integrate Qwen models, and deliver a secure multi-agent network engineering platform leveraging proven VS Code infrastructure**