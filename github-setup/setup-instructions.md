# GitHub Setup Instructions

## Quick Start: Setting Up Your GitHub Project

### 1. Create GitHub Repository
```bash
# Create new repository on GitHub
Repository Name: ai-dating-platform-mvp
Description: AI-Powered African Dating Platform - Cross-cultural dating with AI coaching
Visibility: Private (for now)
Initialize with README: Yes
```

### 2. Set Up Labels (Copy/Paste Ready)

Navigate to your repository → Issues → Labels → New Label

#### Issue Types (Blue #0052CC)
```
epic - Major feature areas containing multiple user stories
user-story - Individual features or improvements
bug - Issues and defects that need fixing
task - Technical work (refactoring, setup, maintenance)
research - Investigation or spike work needed
```

#### Priority Levels (Red #E53E3E)
```
priority: p0-critical - MVP blockers, security issues, system down
priority: p1-high - Core dating features, user-blocking issues
priority: p2-medium - Enhancement features, nice improvements
priority: p3-low - Nice-to-have features, cosmetic fixes
```

#### Epic Categories (Purple #805AD5)
```
epic: foundation - Development environment, CI/CD, basic setup
epic: user-profiles - Registration, profiles, photos, verification
epic: ai-coaching - Cultural coaching system and AI personas
epic: matching-system - Compatibility assessment and algorithms
epic: messaging - Real-time communication features
epic: safety-trust - Fraud detection, safety, moderation
epic: payments - Subscriptions, billing, premium features
epic: launch-prep - Production readiness, optimization, marketing
```

#### Agent Assignments (Green #38A169)
```
agent: ai-coaching-specialist - AI coaching features and personas
agent: matching-specialist - Compatibility algorithms and matching
agent: frontend-specialist - React components and UI
agent: design-reviewer - UI/UX review and validation
agent: troubleshooter - Debug and fix issues with Telescope
agent: safety-specialist - Security, fraud detection, moderation
```

#### Technical Categories (Teal #319795)
```
backend: laravel - Laravel backend development work
frontend: react - React frontend development work
database: postgresql - Database schema and query work
realtime: reverb - WebSocket and real-time features
mobile: responsive - Mobile-first responsive design
```

#### Cultural & UX (Orange #DD6B20)
```
cultural-review - Requires cultural sensitivity review
mobile-critical - Must work perfectly on mobile devices
multi-language - English/Chinese language support
cross-cultural - Cross-cultural relationship features
```

### 3. Create Project Board

Go to Projects → New Project → Board

**Project Name**: AI Dating Platform MVP
**Description**: 16-week sprint plan for cross-cultural dating platform

#### Columns:
1. 📋 Backlog
2. 🎯 Ready
3. 🔄 In Progress
4. 👀 Code Review
5. 🎨 Design Review
6. 🧪 Testing
7. 🚀 Ready to Deploy
8. ✅ Done

#### Custom Fields:
- **Epic**: Single select dropdown
- **Priority**: Single select (P0, P1, P2, P3)
- **Agent**: Multi-select
- **Sprint**: Text field
- **Story Points**: Number
- **Cultural Review**: Checkbox
- **Mobile Ready**: Checkbox

### 4. Create Milestones

Navigate to Issues → Milestones → New Milestone

```
Sprint 1 - Foundation (Weeks 1-2)
Due Date: [2 weeks from start]
Description: Development environment setup and Claude Agent Framework integration

Sprint 2 - User Profiles (Weeks 3-4)
Due Date: [4 weeks from start]
Description: Complete user registration and profile system for all user types

Sprint 3 - Matching (Weeks 5-6)
Due Date: [6 weeks from start]
Description: Psychology-based compatibility assessment and matching system

Sprint 4 - Messaging (Weeks 7-8)
Due Date: [8 weeks from start]
Description: Real-time messaging system with safety features
```

### 5. Create Issue Templates

Go to Settings → Features → Issues → Set up templates

Create these 3 templates:

#### Epic Template (`epic-template.md`)
```yaml
---
name: Epic Template
about: Major feature area containing multiple user stories
title: '[EPIC] Feature Name'
labels: 'epic, priority: p1-high'
---

## Epic Overview
Brief description of the major feature area

## Business Value
Why this epic matters for the dating platform MVP

## User Types Affected
- [ ] African Women (Free Users)
- [ ] Chinese Men (Premium Users)
- [ ] Western Men (Premium Users)

## Cultural Considerations
- Cultural sensitivity requirements
- Multi-language support needs
- Cross-cultural UX considerations

## Success Criteria
- Measurable outcomes
- User satisfaction metrics
- Performance benchmarks

## User Stories
- [ ] #issue-number - Story title
- [ ] #issue-number - Story title

## Definition of Done
- [ ] All user stories completed
- [ ] Cultural review passed
- [ ] Mobile experience optimized
- [ ] Performance benchmarks met
```

#### User Story Template (`user-story-template.md`)
```yaml
---
name: User Story Template
about: Individual feature or improvement
title: '[STORY] As a [user type], I want to [action] so that [benefit]'
labels: 'user-story, priority: p2-medium'
---

## User Story
**As a** [user type]
**I want to** [capability]
**So that** [benefit]

## Epic
[Link to parent epic]

## Acceptance Criteria
- [ ] Criteria 1
- [ ] Criteria 2
- [ ] Criteria 3

## Cultural Considerations
- Any cultural sensitivity requirements
- Multi-language support needs
- Cross-cultural UX considerations

## Technical Requirements
- Frontend: React components needed
- Backend: Laravel features needed
- Database: Schema changes required
- Agents: Which agents will work on this

## Commands for Agents
```bash
/build "[story description]"  # For development
/debug "[issue description]"  # If problems arise
/design-review              # For UI/UX validation
```

## Definition of Done
- [ ] Acceptance criteria met
- [ ] Tests passing (unit + feature + mobile)
- [ ] Code reviewed and approved
- [ ] Design review completed via `/design-review`
- [ ] Cultural review completed (if needed)
- [ ] Deployed to staging environment
```

#### Bug Template (`bug-template.md`)
```yaml
---
name: Bug Report
about: Report a bug or issue
title: '[BUG] Brief description'
labels: 'bug, priority: p1-high'
---

## Bug Description
Clear description of the issue

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected vs Actual Behavior
**Expected**: What should happen
**Actual**: What actually happens

## Environment
- Browser: [Chrome/Safari/Firefox]
- Device: [Mobile/Desktop]
- User Type: [African Woman/Chinese Man/Western Man]

## Laravel Telescope Investigation
```bash
/debug "[bug description]"
```
Check localhost:8020/telescope for:
- [ ] Request errors
- [ ] Database query issues
- [ ] Queue job failures
- [ ] Exception details

## Priority Assessment
- [ ] P0 - Blocks user registration/payments
- [ ] P1 - Affects core dating functionality
- [ ] P2 - Minor UX issue
- [ ] P3 - Cosmetic issue
```

### 6. Create First Sprint Issues

Copy and paste these initial issues:

#### Epic Issue 1:
```
Title: [EPIC] Development Environment Setup
Labels: epic, priority: p0-critical, epic: foundation, sprint: week-1-2
Milestone: Sprint 1 - Foundation (Weeks 1-2)
Assignees: [Your username]

[Paste Epic Overview content from epic-issues.md]
```

#### User Story Issues for Sprint 1:
```
Title: [STORY] Laravel + React Development Environment Setup
Labels: user-story, priority: p0-critical, epic: foundation, agent: troubleshooter, backend: laravel, frontend: react
Milestone: Sprint 1 - Foundation (Weeks 1-2)

[Paste user story content from user-stories.md]
```

### 7. Set Up Project Automation (GitHub Actions)

Create `.github/workflows/issue-automation.yml`:

```yaml
name: Issue Automation
on:
  issues:
    types: [opened, labeled]

jobs:
  auto-assign-project:
    runs-on: ubuntu-latest
    steps:
      - name: Add to Project Board
        uses: actions/add-to-project@v0.4.0
        with:
          project-url: https://github.com/users/[username]/projects/[project-number]
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

### 8. Integration with Agent System

Add this to your repository `.claude/settings.json`:

```json
{
  "project_tracking": {
    "github_repo": "your-username/ai-dating-platform-mvp",
    "project_board_url": "https://github.com/users/your-username/projects/1",
    "issue_creation_enabled": true,
    "agent_command_tracking": true
  },
  "sprint_settings": {
    "current_sprint": "Sprint 1 - Foundation (Weeks 1-2)",
    "sprint_length_weeks": 2,
    "story_point_capacity": 25
  }
}
```

### 9. Daily Workflow

#### Start of Sprint:
1. Review backlog and move issues to "Ready"
2. Assign issues to team members
3. Set up Sprint milestone
4. Kick off with first `/build` command

#### During Development:
1. Move issues through project board columns
2. Use agent commands in issue comments:
   ```bash
   /build "user registration system"
   /debug "telescope configuration issue"
   /design-review  # After UI implementation
   ```
3. Update issue status and add progress comments
4. Create new issues for discovered work

#### End of Sprint:
1. Review completed work against success criteria
2. Move remaining issues to next sprint
3. Conduct cultural sensitivity review
4. Update sprint metrics and velocity

### 10. Success Metrics Dashboard

Track these metrics in your project:

#### Sprint Velocity
- Story points completed per sprint
- Issue completion rate
- Agent command usage frequency

#### Cultural Sensitivity
- Issues requiring cultural review
- Cultural sensitivity approval rate
- Cross-cultural user feedback

#### Mobile Performance
- Mobile-critical issues completion
- Mobile test passing rate
- Mobile user experience rating

This setup gives you a complete project management system integrated with your Claude Agent Framework for rapid, culturally-sensitive dating platform development! 🚀