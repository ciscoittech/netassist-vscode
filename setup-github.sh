#!/bin/bash

# NetAssist GitHub Repository Setup Script
# This script initializes and pushes the NetAssist project to GitHub

set -e

echo "🚀 NetAssist GitHub Repository Setup"
echo "====================================="

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

# Check if GitHub CLI is installed (optional but recommended)
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI found"
    HAS_GH_CLI=true
else
    echo "⚠️  GitHub CLI not found (install with: brew install gh)"
    HAS_GH_CLI=false
fi

# Get repository details
echo ""
echo "📋 Repository Configuration"
read -p "GitHub username: " GITHUB_USERNAME
read -p "Repository name [netassist-vscode]: " REPO_NAME
REPO_NAME=${REPO_NAME:-netassist-vscode-extension}

read -p "Repository description [AI-powered network engineering assistant for VS Code]: " REPO_DESC
REPO_DESC=${REPO_DESC:-"AI-powered network engineering assistant for VS Code with secure IP sanitization, multi-agent orchestration, and enterprise security features"}

read -p "Make repository private initially? [y/N]: " MAKE_PRIVATE
MAKE_PRIVATE=${MAKE_PRIVATE:-n}

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
    git commit -m "feat: initial NetAssist VS Code extension with IP sanitization

- Complete VS Code extension foundation
- FastAPI IP sanitization server
- Network-specific AI modes (Config, Troubleshoot, Validate, Document)
- OpenRouter integration with Qwen models
- Security-first architecture with audit logging
- Docker deployment support
- Comprehensive documentation and tests

🔒 Features secure IP sanitization for network engineers
🚀 Ready for development and testing"
    echo "✅ Initial commit created"
else
    echo "✅ Repository already has commits"
fi

# Create GitHub repository
echo ""
echo "🌐 Creating GitHub repository..."

if [ "$HAS_GH_CLI" = true ]; then
    # Use GitHub CLI (easier)
    VISIBILITY_FLAG=""
    if [ "$MAKE_PRIVATE" = "y" ] || [ "$MAKE_PRIVATE" = "Y" ]; then
        VISIBILITY_FLAG="--private"
    else
        VISIBILITY_FLAG="--public"
    fi

    if gh repo create "$GITHUB_USERNAME/$REPO_NAME" $VISIBILITY_FLAG --description "$REPO_DESC" --source . --push; then
        echo "✅ GitHub repository created and pushed successfully!"
        REPO_URL="https://github.com/$GITHUB_USERNAME/$REPO_NAME"
    else
        echo "❌ Failed to create repository with GitHub CLI"
        exit 1
    fi
else
    # Manual setup instructions
    echo "📝 Manual GitHub Setup Required:"
    echo ""
    echo "1. Go to https://github.com/new"
    echo "2. Repository name: $REPO_NAME"
    echo "3. Description: $REPO_DESC"
    if [ "$MAKE_PRIVATE" = "y" ] || [ "$MAKE_PRIVATE" = "Y" ]; then
        echo "4. Visibility: Private"
    else
        echo "4. Visibility: Public"
    fi
    echo "5. Don't initialize with README (we already have files)"
    echo "6. Click 'Create repository'"
    echo ""
    read -p "Press Enter after creating the repository on GitHub..."

    # Add remote and push
    REPO_URL="https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
    git remote add origin "$REPO_URL"
    git branch -M main
    git push -u origin main

    echo "✅ Repository pushed to GitHub"
    REPO_URL="https://github.com/$GITHUB_USERNAME/$REPO_NAME"
fi

# Setup branch protection (if using GitHub CLI)
if [ "$HAS_GH_CLI" = true ]; then
    echo ""
    echo "🛡️  Setting up branch protection..."

    # Wait a moment for repository to be fully created
    sleep 2

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
fi

# Create development branch
echo ""
echo "🌿 Creating development branch..."
git checkout -b develop
git push -u origin develop
git checkout main

echo "✅ Development branch created"

# Setup GitHub labels
if [ "$HAS_GH_CLI" = true ]; then
    echo ""
    echo "🏷️  Setting up GitHub labels..."

    # Remove default labels and add custom ones
    gh label create "security" --description "Security-related issues" --color "d73a4a" --force
    gh label create "sanitization" --description "IP/credential sanitization" --color "0075ca" --force
    gh label create "ai-models" --description "AI model integration" --color "7057ff" --force
    gh label create "network-modes" --description "Network-specific modes" --color "008672" --force
    gh label create "ui/ux" --description "User interface improvements" --color "d876e3" --force
    gh label create "performance" --description "Performance improvements" --color "fbca04" --force
    gh label create "documentation" --description "Documentation updates" --color "0052cc" --force

    echo "✅ Custom labels created"
fi

# Create NetAssist epics and initial issues
if [ "$HAS_GH_CLI" = true ]; then
    echo ""
    echo "📋 Creating NetAssist epics and Sprint 1 issues..."

    # Epic 1: Foundation & Extension Architecture
    gh issue create \
        --title "[EPIC] VS Code Extension Foundation with Agent System" \
        --body "$(cat github-setup/netassist-epic-issues.md | head -100)" \
        --label "epic,priority: p0-critical,sprint: week-1-2,component: foundation"

    # Sprint 1 User Stories
    gh issue create \
        --title "[STORY] Install NetAssist extension with secure foundation" \
        --body "**As a** network engineer
**I want to** install NetAssist extension
**So that** I can get AI assistance for network tasks with enterprise security

## Acceptance Criteria
- [ ] Extension installs from .vsix package
- [ ] FastAPI sanitization server starts automatically
- [ ] Agent system loads without errors
- [ ] Security status indicator shows 'Protected'

## Agent Assignment
- architect: Extension architecture design
- engineer: VS Code extension implementation
- network-specialist: Security requirements validation" \
        --label "user-story,priority: p0-critical,sprint: week-1-2,agent: architect,component: foundation"

    gh issue create \
        --title "[STORY] Automatic IP sanitization for safe AI processing" \
        --body "**As a** network engineer
**I want to** have my IP addresses automatically sanitized
**So that** I can safely use AI without security risks

## Acceptance Criteria
- [ ] All IPv4/IPv6 addresses replaced before cloud API calls
- [ ] Network ranges and subnets properly sanitized
- [ ] Original values restored in AI responses
- [ ] Sanitization audit log maintained

## Agent Assignment
- network-specialist: Sanitization patterns and algorithms
- api-specialist: FastAPI endpoint implementation
- reviewer: Security validation and testing" \
        --label "user-story,priority: p0-critical,sprint: week-1-2,agent: network-specialist,component: sanitization"

    gh issue create \
        --title "[STORY] Dynamic network agent loading based on configuration type" \
        --body "**As a** network engineer
**I want to** have network specialist agents loaded automatically
**So that** I get relevant expertise based on my configuration type

## Acceptance Criteria
- [ ] Cisco config detected → cisco-specialist agent loaded
- [ ] Linux iptables detected → linux-specialist agent loaded
- [ ] Cloud config detected → cloud-specialist agent loaded
- [ ] Multiple agents can be active simultaneously

## Agent Assignment
- architect: Agent loading strategy and orchestration
- engineer: Agent detection and routing logic
- network-specialist: Configuration type detection patterns" \
        --label "user-story,priority: p1-high,sprint: week-1-2,agent: architect,component: agents"

    echo "✅ NetAssist epics and initial Sprint 1 issues created"
fi

# Final instructions
echo ""
echo "🎉 GitHub Repository Setup Complete!"
echo "===================================="
echo ""
echo "📍 Repository URL: $REPO_URL"
echo "🌿 Branches: main (protected), develop"
echo "🏷️  Labels: Custom labels for NetAssist development"
echo "📋 Issues: Initial development tasks created"
echo ""
echo "🚀 Next Steps:"
echo "1. Clone the repository locally:"
echo "   git clone $REPO_URL.git"
echo ""
echo "2. Setup development environment:"
echo "   cd $REPO_NAME"
echo "   npm install"
echo "   ./start.sh"
echo ""
echo "3. Start developing:"
echo "   git checkout develop"
echo "   # Make your changes"
echo "   git add ."
echo "   git commit -m 'feat: your feature'"
echo "   git push origin develop"
echo ""
echo "4. Create pull requests to main branch for releases"
echo ""
echo "📚 Documentation:"
echo "- README.md: User guide and setup"
echo "- DEVELOPMENT.md: Developer guide"
echo "- CONTRIBUTING.md: Contribution guidelines"
echo ""
echo "🔒 Security:"
echo "- Never commit API keys or real network data"
echo "- All network configs go through sanitization"
echo "- Follow security guidelines in CONTRIBUTING.md"
echo ""
echo "💡 Pro Tips:"
echo "- Use 'gh repo view --web' to open repository in browser"
echo "- Use 'gh issue list' to see development tasks"
echo "- Use 'gh pr create' to create pull requests"
echo ""
echo "Happy coding! 🚀"