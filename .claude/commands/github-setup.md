# NetAssist GitHub Setup Command

## Purpose
Create and configure private GitHub repository with NetAssist-specific epics, issues, and workflows

## Agents Required
- **architect**: Design repository structure and epic organization
- **engineer**: Implement GitHub Actions workflows and automation
- **reviewer**: Security review of repository configuration and access controls

## Execution Strategy

### Phase 1: Repository Creation (Parallel)
```bash
# Create private repository with proper structure
architect: Design repository organization and branch strategy
engineer: Execute GitHub CLI repository creation
reviewer: Validate security settings and access controls
```

### Phase 2: Epic and Issue Creation (Sequential)
```bash
# Load NetAssist-specific epics from github-setup/
engineer: Create 8 NetAssist epics from epic-issues design
engineer: Generate initial issues for Sprint 1 (Foundation)
architect: Validate epic structure and dependencies
```

### Phase 3: Workflow Configuration (Parallel)
```bash
# Setup CI/CD and automation
engineer: Create GitHub Actions for testing and building
engineer: Setup branch protection and PR templates
reviewer: Configure security scanning and compliance workflows
```

## GitHub Repository Configuration

### Repository Settings
- **Name**: `netassist-vscode-extension`
- **Visibility**: Private (enterprise security requirement)
- **Description**: "AI-powered network engineering assistant for VS Code with secure IP sanitization"
- **Topics**: `vscode-extension`, `network-engineering`, `ip-sanitization`, `ai-assistant`, `security`

### Branch Strategy
- **main**: Production releases only
- **develop**: Active development branch
- **feature/***: Individual epic/feature branches
- **hotfix/***: Critical production fixes

### Security Configuration
- Branch protection on `main` and `develop`
- Required PR reviews (minimum 1)
- Required status checks: test-extension, test-sanitization-server, security-scan
- Dismiss stale reviews when new commits are pushed
- Restrict pushes to administrators only

## Epic Structure Implementation

### Epic Categories (8 Total)
1. **Foundation & Extension Architecture** - Core VS Code + agent system
2. **IP Sanitization & Security Layer** - Enterprise security foundation
3. **Multi-Agent Network Intelligence** - Dynamic agent coordination
4. **Network Workflow Builder Engine** - AI workflow creation
5. **Network Tool Orchestration** - pyATS and tool integration
6. **Enterprise Security & Compliance** - Audit and compliance features
7. **Network Mode Specialization** - Config/Troubleshoot/Validate/Document
8. **MVP Launch & Optimization** - Production readiness

### Issue Labeling System
- **Epic Labels**: `epic`, `priority: p0-critical`, `sprint: week-X-Y`
- **Agent Labels**: `agent: architect`, `agent: network-specialist`, etc.
- **Domain Labels**: `network: cisco`, `network: security`, `network: cloud`
- **Component Labels**: `component: vscode`, `component: fastapi`, `component: sanitization`

## GitHub Actions Workflows

### Testing Workflow
```yaml
name: NetAssist Test Suite
on: [push, pull_request]
jobs:
  test-extension:
    # TypeScript/VS Code extension tests
  test-sanitization-server:
    # Python/FastAPI tests
  security-scan:
    # Network security and sanitization validation
```

### Build and Package Workflow
```yaml
name: NetAssist Build
on: [release]
jobs:
  build-extension:
    # Package .vsix file
  build-sanitizer:
    # Docker container build
  publish-release:
    # GitHub releases with artifacts
```

## Commands for Execution

### Initial Repository Setup
```bash
# Run the enhanced GitHub setup script
./setup-github.sh
# This creates repository, sets up epics, configures security
```

### Epic Management
```bash
# Create all NetAssist epics
gh issue create --template epic-template.md --title "[EPIC] Foundation & Extension Architecture"
# Repeat for all 8 epics with appropriate labels and assignments
```

### Sprint Planning
```bash
# Create Sprint 1 issues (Weeks 1-2)
/github-sprint "Sprint 1" "Foundation & Extension Architecture"
# This creates individual user stories from epic breakdown
```

## Success Criteria

### Repository Configuration
- Private repository created with proper access controls
- Branch protection rules active on main/develop
- All 8 NetAssist epics created and properly labeled
- Initial Sprint 1 issues ready for development

### Security Validation
- No sensitive network data in repository (sanitization examples only)
- Security scanning workflows active
- Access controls properly configured
- Audit logging enabled for repository activities

### Agent Integration
- Agent assignments mapped to GitHub issues via labels
- Commands integrated with GitHub workflows
- Epic structure aligns with .claude-library agent capabilities

### Development Readiness
- GitHub Actions workflows functional
- PR templates configured for proper review process
- Issue templates ready for efficient issue creation
- Sprint planning structure supports agile development

## Network Engineering Focus

### Issue Templates Customized For:
- **Network Configuration Issues**: Cisco/Juniper/Linux specific templates
- **Security Vulnerabilities**: Network-specific security review process
- **Performance Issues**: Network processing optimization templates
- **Compliance Issues**: Enterprise audit and compliance tracking

### Epic Progression Strategy
- **Sprint 1-2**: Foundation (VS Code + FastAPI + Security)
- **Sprint 3-4**: Core Intelligence (Agent system + Sanitization)
- **Sprint 5-6**: Network Tools (pyATS + Workflow Builder)
- **Sprint 7-8**: Enterprise Features (Compliance + Launch)

## Integration with Agent System

The GitHub setup integrates seamlessly with our .claude-library agents:
- **Issues tagged with agent labels** automatically route to appropriate specialists
- **Epic progress tracked** through agent completion status
- **Commands available** for GitHub operations from VS Code
- **Security reviews required** for all network-related changes