# GitHub Projects Setup Guide

## Project Board Configuration

### Main Project: "AI Dating Platform MVP"
**Project Type**: Board View with Custom Fields

#### Columns (Status Flow):
1. **📋 Backlog** - New issues awaiting prioritization
2. **🎯 Ready** - Prioritized and ready for development
3. **🔄 In Progress** - Currently being worked on
4. **👀 Code Review** - Ready for PR review
5. **🎨 Design Review** - UI/UX review needed
6. **🧪 Testing** - QA and user testing phase
7. **🚀 Ready to Deploy** - Approved and ready for production
8. **✅ Done** - Completed and deployed

#### Custom Fields:
- **Epic**: Dropdown (User Profiles, AI Coaching, Matching, Messaging, Safety, Payments)
- **Priority**: Dropdown (P0-Critical, P1-High, P2-Medium, P3-Low)
- **Agent**: Multi-select (ai-coaching-specialist, frontend-specialist, etc.)
- **Sprint**: Text (Week 1-2, Week 3-4, etc.)
- **Story Points**: Number (1, 2, 3, 5, 8)
- **Cultural Review**: Checkbox (Needs cultural sensitivity review)
- **Mobile Ready**: Checkbox (Mobile-first design completed)

## Issue Templates

### Epic Template
```markdown
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

## Dependencies
- Dependencies on other epics or external services

## Definition of Done
- [ ] All user stories completed
- [ ] Cultural review passed
- [ ] Mobile experience optimized
- [ ] Performance benchmarks met
```

### User Story Template
```markdown
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

## Design Requirements
- [ ] Mobile-first responsive design (375px+)
- [ ] shadcn/ui component consistency
- [ ] Accessibility requirements met
- [ ] Cultural UI considerations addressed

## Testing Requirements
- [ ] Unit tests for business logic
- [ ] Feature tests for user flows
- [ ] Mobile responsive testing
- [ ] Cultural sensitivity testing

## Definition of Done
- [ ] Acceptance criteria met
- [ ] Tests passing (unit + feature + mobile)
- [ ] Code reviewed and approved
- [ ] Design review completed via `/design-review`
- [ ] Cultural review completed (if needed)
- [ ] Deployed to staging environment
- [ ] Product owner approval received

## Commands for Agents
```bash
/build "[story description]"  # For development
/debug "[issue description]"  # If problems arise
/design-review              # For UI/UX validation
```
```

### Bug Template
```markdown
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

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- Browser: [Chrome/Safari/Firefox]
- Device: [Mobile/Desktop]
- User Type: [African Woman/Chinese Man/Western Man]

## Screenshots
[Add screenshots if applicable]

## Laravel Telescope Investigation
```bash
/debug "[bug description]"
```
Check localhost:8020/telescope for:
- [ ] Request errors
- [ ] Database query issues
- [ ] Queue job failures
- [ ] Exception details

## Cultural Context
- Does this affect cross-cultural features?
- Any cultural sensitivity concerns?

## Priority Assessment
- [ ] P0 - Blocks user registration/payments
- [ ] P1 - Affects core dating functionality
- [ ] P2 - Minor UX issue
- [ ] P3 - Cosmetic issue
```

## Labels Structure

### Issue Types
- `epic` - Major feature areas
- `user-story` - Individual features
- `bug` - Issues and defects
- `task` - Technical work (refactoring, setup)
- `research` - Investigation needed

### Priority Levels
- `priority: p0-critical` - MVP blockers, security issues
- `priority: p1-high` - Core dating features
- `priority: p2-medium` - Enhancement features
- `priority: p3-low` - Nice-to-have features

### Epic Categories
- `epic: user-profiles` - Registration, profiles, photos
- `epic: ai-coaching` - Cultural coaching system
- `epic: matching-system` - Compatibility and matching
- `epic: messaging` - Real-time communication
- `epic: safety-trust` - Fraud detection, safety
- `epic: payments` - Subscriptions and billing

### Agent Assignments
- `agent: ai-coaching-specialist` - AI coaching features
- `agent: matching-specialist` - Compatibility algorithms
- `agent: frontend-specialist` - React components
- `agent: design-reviewer` - UI/UX review
- `agent: troubleshooter` - Debug and fix issues
- `agent: safety-specialist` - Security and fraud detection

### Technical Categories
- `backend: laravel` - Laravel backend work
- `frontend: react` - React frontend work
- `database: postgresql` - Database changes
- `realtime: reverb` - WebSocket features
- `ai: coaching` - AI integration work
- `payments: stripe` - Payment processing

### Special Labels
- `needs-cultural-review` - Requires cultural sensitivity review
- `mobile-critical` - Must work perfectly on mobile
- `performance-sensitive` - Needs optimization
- `security-sensitive` - Security implications
- `blocked` - Cannot proceed due to dependency

## Milestones

### Sprint Structure (2-week sprints)
- **Sprint 1 (Weeks 1-2)**: Foundation Setup
- **Sprint 2 (Weeks 3-4)**: Core User Profiles
- **Sprint 3 (Weeks 5-6)**: Basic Matching System
- **Sprint 4 (Weeks 7-8)**: Real-time Messaging
- **Sprint 5 (Weeks 9-10)**: AI Cultural Coaching
- **Sprint 6 (Weeks 11-12)**: Safety & Trust Features
- **Sprint 7 (Weeks 13-14)**: Payment Integration
- **Sprint 8 (Weeks 15-16)**: MVP Polish & Launch

### Major Release Milestones
- **v0.1 - Foundation**: Basic Laravel + React setup
- **v0.2 - Profiles**: User registration and profiles
- **v0.3 - Matching**: Core matching functionality
- **v0.4 - Communication**: Real-time messaging
- **v0.5 - AI Coaching**: Cultural coaching system
- **v0.6 - Safety**: Trust and safety features
- **v0.7 - Payments**: Subscription system
- **v1.0 - MVP Launch**: Full dating platform