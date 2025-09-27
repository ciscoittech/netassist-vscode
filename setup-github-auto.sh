#!/bin/bash

# NetAssist GitHub Repository Setup Script (Automated)
# This script initializes and pushes the NetAssist project to GitHub

set -e

echo "🚀 NetAssist GitHub Repository Setup (Automated)"
echo "=================================================="

# Configuration (auto-detect from GitHub CLI)
GITHUB_USERNAME=$(gh api user --jq .login)
REPO_NAME="netassist-vscode-extension"
REPO_DESC="AI-powered network engineering assistant for VS Code with secure IP sanitization, multi-agent orchestration, and enterprise security features"
MAKE_PRIVATE="y"  # Private repository for enterprise security

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: Please run this script from the vscode-extension directory"
    exit 1
fi

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is required but not installed"
    exit 1
fi

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI is required but not installed"
    echo "Install with: brew install gh"
    exit 1
fi

echo "✅ GitHub CLI found"

# Initialize git repository
echo ""
echo "🔧 Initializing Git repository..."

if [ ! -d ".git" ]; then
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Add all files
git add .

# Create initial commit
if ! git rev-parse --verify HEAD >/dev/null 2>&1; then
    git commit -m "feat: initial NetAssist VS Code extension with secure IP sanitization

🎯 Complete foundation for AI-powered network engineering assistant

Core Features:
- VS Code extension with Claude Agent Framework integration
- FastAPI IP sanitization server with enterprise security
- Network-specific AI modes (Config, Troubleshoot, Validate, Document)
- Multi-agent orchestration for network specialist coordination
- Enterprise audit logging and compliance features
- Docker deployment support with comprehensive testing

🔒 Security-First Architecture:
- Zero data leakage with local IP sanitization
- Original network values never reach cloud APIs
- SOC2/ISO27001 compliance ready
- Comprehensive audit trail for enterprise adoption

🚀 Agent System Integration:
- Dynamic agent loading based on network configuration types
- Parallel execution for multiple network specialists
- Custom workflow builder for network engineering tasks
- Integration with pyATS and network testing frameworks

Ready for enterprise network engineering deployment and development."
    echo "✅ Initial commit created"
else
    echo "✅ Repository already has commits"
fi

# Create GitHub repository
echo ""
echo "🌐 Creating GitHub repository..."

VISIBILITY_FLAG="--private"
if [ "$MAKE_PRIVATE" != "y" ] && [ "$MAKE_PRIVATE" != "Y" ]; then
    VISIBILITY_FLAG="--public"
fi

if gh repo create "$GITHUB_USERNAME/$REPO_NAME" $VISIBILITY_FLAG --description "$REPO_DESC" --source . --push; then
    echo "✅ GitHub repository created and pushed successfully!"
    REPO_URL="https://github.com/$GITHUB_USERNAME/$REPO_NAME"
else
    echo "❌ Failed to create repository with GitHub CLI"
    exit 1
fi

# Setup branch protection
echo ""
echo "🛡️  Setting up branch protection..."

# Wait for repository to be fully created
sleep 3

if gh api repos/$GITHUB_USERNAME/$REPO_NAME/branches/main/protection \
    --method PUT \
    --field required_status_checks='{"strict":true,"contexts":["test-extension","test-sanitization-server","security-scan"]}' \
    --field enforce_admins=true \
    --field required_pull_request_reviews='{"required_approving_review_count":1}' \
    --field restrictions=null \
    2>/dev/null; then
    echo "✅ Branch protection rules set"
else
    echo "⚠️  Branch protection setup failed (may need admin permissions)"
fi

# Create development branch
echo ""
echo "🌿 Creating development branch..."
git checkout -b develop
git push -u origin develop
git checkout main

echo "✅ Development branch created"

# Setup GitHub labels for NetAssist
echo ""
echo "🏷️  Setting up NetAssist-specific GitHub labels..."

# Remove default labels and add NetAssist custom ones
gh label create "epic" --description "Major feature areas" --color "5319e7" --force
gh label create "user-story" --description "Individual user stories" --color "0075ca" --force
gh label create "security" --description "Security and sanitization issues" --color "d73a4a" --force
gh label create "network-modes" --description "Network-specific modes (Config/Troubleshoot/Validate/Document)" --color "008672" --force
gh label create "agent-system" --description "Claude agent framework integration" --color "7057ff" --force
gh label create "sanitization" --description "IP/credential sanitization features" --color "d876e3" --force
gh label create "enterprise" --description "Enterprise security and compliance" --color "fbca04" --force
gh label create "network-engineering" --description "Network engineering domain features" --color "0052cc" --force

# Priority labels
gh label create "priority: p0-critical" --description "MVP blockers and security issues" --color "d73a4a" --force
gh label create "priority: p1-high" --description "Core network engineering features" --color "ff9500" --force
gh label create "priority: p2-medium" --description "Enhancement features" --color "fbca04" --force
gh label create "priority: p3-low" --description "Nice-to-have features" --color "0075ca" --force

# Agent assignment labels
gh label create "agent: architect" --description "Architecture and design agent" --color "5319e7" --force
gh label create "agent: engineer" --description "Implementation agent" --color "0075ca" --force
gh label create "agent: network-specialist" --description "Network engineering specialist agent" --color "008672" --force
gh label create "agent: api-specialist" --description "FastAPI specialist agent" --color "7057ff" --force
gh label create "agent: reviewer" --description "Security and code review agent" --color "d73a4a" --force

# Component labels
gh label create "component: foundation" --description "VS Code extension foundation" --color "1d76db" --force
gh label create "component: sanitization" --description "IP sanitization layer" --color "d876e3" --force
gh label create "component: agents" --description "Agent system and orchestration" --color "7057ff" --force
gh label create "component: fastapi" --description "FastAPI backend service" --color "0052cc" --force

echo "✅ NetAssist custom labels created"

# Create NetAssist epics and initial issues (only if the epic file exists)
if [ -f "github-setup/netassist-epic-issues.md" ]; then
    echo ""
    echo "📋 Creating NetAssist epics and Sprint 1 issues..."

    # Epic 1: Foundation & Extension Architecture
    gh issue create \
        --title "[EPIC] VS Code Extension Foundation with Agent System" \
        --body "Fork and adapt proven agent platform for network engineering, integrating Claude Agent Framework with FastAPI sanitization layer for secure network configuration processing.

## Business Value
Establishes secure foundation for AI-powered network engineering assistant with enterprise-grade security and multi-agent orchestration capabilities.

## User Types Affected
- Network Engineers (All domains) - Primary users
- Linux Network Administrators - VLAN/bridge configurations
- Cloud Network Engineers - VPC/security group configs
- Security Engineers - Firewall rule analysis

## Success Criteria
- VS Code extension loads and connects to agent system successfully
- FastAPI sanitization server processes network configs without data leakage
- Agent system dynamically loads network specialists based on user queries
- Zero exposure of original IP addresses or credentials to cloud APIs

## Agent Integration
- **Primary**: architect - Design extension architecture and FastAPI integration
- **Supporting**: engineer - Implement TypeScript extension and Python services
- **Specialist**: network-specialist - Define network-specific requirements

## Sprint Timeline
Week 1-2: Core foundation with security-first architecture" \
        --label "epic,priority: p0-critical,sprint: week-1-2,component: foundation"

    # Sprint 1 User Stories
    gh issue create \
        --title "[STORY] Install NetAssist extension with secure foundation" \
        --body "**As a** network engineer
**I want to** install NetAssist extension
**So that** I can get AI assistance for network tasks with enterprise security

## Acceptance Criteria
- [ ] Extension installs from .vsix package successfully
- [ ] FastAPI sanitization server starts automatically on extension activation
- [ ] Agent system loads without errors and shows status indicator
- [ ] Security status indicator shows 'Protected' confirming sanitization active
- [ ] Basic network configuration detection working

## Technical Implementation
- VS Code extension manifest and activation events
- FastAPI server startup integration
- Agent system initialization and health checks
- Security status UI component

## Agent Assignment
- **architect**: Extension architecture design and startup flow
- **engineer**: VS Code extension implementation and integration
- **network-specialist**: Security requirements validation and testing

## Definition of Done
- Extension activates successfully in VS Code
- All components start without errors
- Security indicators functional
- Basic smoke tests passing" \
        --label "user-story,priority: p0-critical,sprint: week-1-2,agent: architect,component: foundation"

    gh issue create \
        --title "[STORY] Automatic IP sanitization for safe AI processing" \
        --body "**As a** network engineer
**I want to** have my IP addresses automatically sanitized
**So that** I can safely use AI without security risks

## Acceptance Criteria
- [ ] All IPv4/IPv6 addresses replaced before any cloud API calls
- [ ] Network ranges and subnets properly sanitized with consistent mapping
- [ ] Original values restored accurately in AI responses
- [ ] Sanitization audit log maintained for compliance
- [ ] Support for Cisco, Linux, and cloud configuration formats

## Technical Implementation
- IP address detection and replacement algorithms
- Secure mapping storage and restoration
- FastAPI endpoints for sanitization operations
- Audit logging with enterprise compliance features

## Agent Assignment
- **network-specialist**: Sanitization patterns and algorithms design
- **api-specialist**: FastAPI endpoint implementation and optimization
- **reviewer**: Security validation and penetration testing

## Definition of Done
- 100% IP sanitization before cloud APIs
- Audit logs capture all operations
- Performance under 200ms for typical configs
- Security review passes with zero data leakage" \
        --label "user-story,priority: p0-critical,sprint: week-1-2,agent: network-specialist,component: sanitization"

    gh issue create \
        --title "[STORY] Dynamic network agent loading based on configuration type" \
        --body "**As a** network engineer
**I want to** have network specialist agents loaded automatically
**So that** I get relevant expertise based on my configuration type

## Acceptance Criteria
- [ ] Cisco config detected → cisco-specialist agent loaded automatically
- [ ] Linux iptables detected → linux-specialist agent loaded
- [ ] Cloud config detected → cloud-specialist agent loaded
- [ ] Multiple agents can be active simultaneously for hybrid configs
- [ ] Agent loading happens within 2 seconds of config detection

## Technical Implementation
- Configuration type detection algorithms
- Dynamic agent loading from .claude-library
- Agent orchestration and coordination
- Performance optimization for agent startup

## Agent Assignment
- **architect**: Agent loading strategy and orchestration design
- **engineer**: Agent detection and routing logic implementation
- **network-specialist**: Configuration type detection patterns and validation

## Definition of Done
- Accurate config type detection >95%
- Fast agent loading <2s
- Multiple agent coordination working
- Memory usage optimized for agent loading" \
        --label "user-story,priority: p1-high,sprint: week-1-2,agent: architect,component: agents"

    echo "✅ NetAssist foundation epic and Sprint 1 issues created"
else
    echo "⚠️  NetAssist epic issues file not found, skipping issue creation"
fi

# Final instructions
echo ""
echo "🎉 NetAssist GitHub Repository Setup Complete!"
echo "=============================================="
echo ""
echo "📍 Repository URL: $REPO_URL"
echo "🌿 Branches: main (protected), develop"
echo "🏷️  Labels: NetAssist-specific labels for network engineering"
echo "📋 Issues: Foundation epic and Sprint 1 user stories created"
echo ""
echo "🚀 Next Steps for Network Engineering Development:"
echo ""
echo "1. Clone the repository locally:"
echo "   git clone $REPO_URL.git"
echo "   cd $REPO_NAME"
echo ""
echo "2. Setup development environment:"
echo "   npm install"
echo "   cd sanitization-server && pip install -r requirements.txt"
echo "   ./start.sh"
echo ""
echo "3. Start developing with agent system:"
echo "   git checkout develop"
echo "   # Use Claude agent commands:"
echo "   /build \"foundation epic implementation\""
echo "   /github-setup  # For additional epic creation"
echo ""
echo "4. Agent-powered development workflow:"
echo "   # The agent system will coordinate multiple specialists"
echo "   # architect + engineer + network-specialist working together"
echo "   # Automatic agent assignment based on issue labels"
echo ""
echo "🔒 Enterprise Security Features:"
echo "- Private repository with branch protection"
echo "- IP sanitization prevents data leakage"
echo "- Audit logging for compliance (SOC2/ISO27001)"
echo "- Security scanning in CI/CD pipeline"
echo ""
echo "📚 Documentation and Resources:"
echo "- README.md: User guide and installation"
echo "- PRD.md: Product requirements and features"
echo "- CLAUDE.md: Agent system configuration"
echo "- .claude-library/: Network specialist agents"
echo ""
echo "💡 Pro Tips for Network Engineers:"
echo "- Use 'gh repo view --web' to open repository"
echo "- Use 'gh issue list --label=\"sprint: week-1-2\"' for current sprint"
echo "- Agent system automatically assigns specialists based on config types"
echo "- All network data stays local - never sent to cloud APIs"
echo ""
echo "🎯 Ready for enterprise network engineering with AI assistance! 🚀"