# AI Team Quick Start Guide
## Get Started with Your AI-Powered Startup Team in 5 Minutes

---

## 🚀 One-Time Setup (5 Minutes)

### Step 1: Copy Files to Central Location
```bash
# Create central AI team directory
cd /Users/Sean/code
mkdir -p .ai-team

# Copy team structure files
cp gutter-tracker/AI_TEAM_STRUCTURE.md .ai-team/
cp -r gutter-tracker/AI_AGENTS .ai-team/

# Optional: Create symlinks in all projects
cd /Users/Sean/code
for dir in */; do
  ln -s ../.ai-team "$dir/.ai-team" 2>/dev/null
done
```

### Step 2: Test with One Agent
```bash
cd /Users/Sean/code/gutter-tracker
claude code

You: "Read .ai-team/AI_AGENTS/DEVOPS_AGENT.md. Run a health check on this app."
```

Done! You now have a full AI team. 🎉

---

## 📞 Quick Reference: Who to Call

| Need | Call This Agent | File to Read |
|------|----------------|--------------|
| **Deploy app** | DevOps/IT Head | `DEVOPS_AGENT.md` |
| **Fix production bug** | DevOps/IT Head | `DEVOPS_AGENT.md` |
| **Build new feature** | Lead Developer | `LEAD_DEV_AGENT.md` |
| **New project idea** | Innovation Lead | `INNOVATION_AGENT.md` |
| **Architecture review** | CTO | `CTO_AGENT.md` |
| **Plan sprint** | Project Manager | `PROJECT_MANAGER_AGENT.md` |
| **Not sure who** | CTO | `CTO_AGENT.md` |

---

## 🎯 Common Scenarios

### Scenario 1: "I have an app idea"
```
Step 1: Innovation Lead
"Read AI_AGENTS/INNOVATION_AGENT.md. Research market for [idea]"
→ Gets validation, competitor analysis

Step 2: CTO
"Read AI_AGENTS/CTO_AGENT.md and [Innovation's research]. Design architecture"
→ Gets technical plan

Step 3: Project Manager
"Read AI_AGENTS/PROJECT_MANAGER_AGENT.md. Create sprint plan for [project]"
→ Gets timeline and tasks

Step 4: Lead Developer
"Read AI_AGENTS/LEAD_DEV_AGENT.md. Start building [feature]"
→ Code gets written

Step 5: DevOps
"Read AI_AGENTS/DEVOPS_AGENT.md. Deploy [project] to production"
→ App goes live
```

### Scenario 2: "Production is down!"
```
Step 1: DevOps (Immediately)
"Read AI_AGENTS/DEVOPS_AGENT.md. Production is down for [app-name]"
→ Diagnoses and fixes

Step 2: Lead Dev (If code bug)
"Read AI_AGENTS/LEAD_DEV_AGENT.md. Fix bug in [file:line]"
→ Creates fix

Step 3: DevOps (Deploy fix)
"Read AI_AGENTS/DEVOPS_AGENT.md. Deploy hotfix"
→ Back online

Step 4: Project Manager (Post-mortem)
"Read AI_AGENTS/PROJECT_MANAGER_AGENT.md. Document incident"
→ Lessons learned
```

### Scenario 3: "Add feature to existing app"
```
Step 1: Lead Developer
"Read AI_AGENTS/LEAD_DEV_AGENT.md and AGENTS.md. Add [feature]"
→ Code implemented

Step 2: Lead Developer (Testing)
"Write tests for [feature]"
→ Tests passing

Step 3: CTO (Review)
"Read AI_AGENTS/CTO_AGENT.md. Review [feature] code"
→ Approved

Step 4: DevOps (Deploy)
"Read AI_AGENTS/DEVOPS_AGENT.md. Deploy latest changes"
→ Live in production
```

---

## 📋 Template Commands

### Copy/Paste These:

#### **DevOps Health Check**
```
Read AI_AGENTS/DEVOPS_AGENT.md. Run a complete health check on all production apps and report status.
```

#### **New Feature Development**
```
Read AI_AGENTS/LEAD_DEV_AGENT.md and AGENTS.md. Implement [feature description] following project patterns.
```

#### **Idea Validation**
```
Read AI_AGENTS/INNOVATION_AGENT.md. Research and validate the market for [idea]. Provide 3 competitors and a go/no-go recommendation.
```

#### **Architecture Review**
```
Read AI_AGENTS/CTO_AGENT.md and AGENTS.md. Review the architecture of this project and provide recommendations for improvement.
```

#### **Sprint Planning**
```
Read AI_AGENTS/PROJECT_MANAGER_AGENT.md. Create a 1-week sprint plan to achieve [goal].
```

---

## 🎓 Learning Path

### Week 1: Get Comfortable
- Day 1-2: Use DevOps agent (health checks, deployments)
- Day 3-4: Use Lead Dev agent (add small feature)
- Day 5: Use Innovation agent (research 1 idea)
- Weekend: Review, reflect

### Week 2: Build Something
- Use PM to plan a small project
- Use CTO to design architecture
- Use Lead Dev to build
- Use DevOps to deploy
- Ship it!

### Week 3: Optimize
- Use full team workflow
- Practice agent handoffs
- Refine your process
- Document lessons learned

### Month 2+: Scale
- Multiple projects
- Smooth agent coordination
- Fast iteration
- Portfolio growing

---

## 💡 Pro Tips

### 1. Always Read the Agent File
```
❌ Bad:  "Deploy this app"
✅ Good: "Read AI_AGENTS/DEVOPS_AGENT.md. Deploy this app following standard procedures"
```

### 2. Provide Context
```
❌ Bad:  "Fix the bug"
✅ Good: "Read AI_AGENTS/LEAD_DEV_AGENT.md and AGENTS.md. Fix bug in routes.py:45 where users can't login"
```

### 3. One Agent Per Session
```
❌ Don't: Switch agent roles mid-session
✅ Do:   End session, start new session with different agent
```

### 4. Use Project AGENTS.md
```
✅ Every agent should read both:
   1. AI_AGENTS/[ROLE]_AGENT.md (their role)
   2. AGENTS.md (project-specific context)
```

### 5. Track in Git
```
git log --oneline -10  # See what agents have done
git commit -m "Add feature X (via Lead Dev agent)"
```

---

## 🔧 Troubleshooting

### "Agent seems confused about its role"
→ Make sure to say "Read AI_AGENTS/[ROLE]_AGENT.md" first

### "Agent doesn't have project context"
→ Also tell it to read "AGENTS.md" in the project

### "Not sure which agent to use"
→ Start with CTO - they can direct you to the right agent

### "Agent is doing tasks outside its role"
→ Remind it: "Stay in your role as [ROLE]. Delegate [task] to [OTHER_AGENT]"

### "Want to switch agents mid-task"
→ Better to finish with current agent, document handoff, start new session

---

## 📂 File Structure Reference

```
/Users/Sean/code/
├── .ai-team/                      # Central AI team docs
│   ├── AI_TEAM_STRUCTURE.md      # Organization chart
│   ├── AI_TEAM_QUICK_START.md    # This file
│   └── AI_AGENTS/                # Agent documentation
│       ├── CTO_AGENT.md          # Chief Technology Officer
│       ├── DEVOPS_AGENT.md       # DevOps/IT Head
│       ├── LEAD_DEV_AGENT.md     # Lead Developer
│       ├── INNOVATION_AGENT.md   # Product Innovation Lead
│       └── PROJECT_MANAGER_AGENT.md # Project Manager
│
└── [your-project]/
    ├── AGENTS.md                  # Project-specific context
    └── .ai-team -> ../.ai-team   # Symlink to team docs
```

---

## ✅ Success Checklist

You know you're using the AI team effectively when:
- [ ] You can deploy without thinking about it (DevOps)
- [ ] Features ship with tests included (Lead Dev)
- [ ] New ideas are validated before building (Innovation)
- [ ] Code follows consistent patterns (CTO)
- [ ] Projects stay on track (Project Manager)
- [ ] You're learning while building (All agents teaching)
- [ ] Your portfolio is growing (Real deployed apps)

---

## 🎯 Next Steps

1. **Today:** Set up .ai-team directory (5 min)
2. **Today:** Test DevOps agent on gutter-tracker
3. **This Week:** Use Innovation agent to find 1 new idea
4. **This Week:** Use Lead Dev agent to add 1 feature
5. **Next Week:** Build a complete project with full team

---

## 📞 Support

**Questions about:**
- Agent roles → Read AI_TEAM_STRUCTURE.md
- Specific agent → Read that agent's .md file
- Project setup → Read project's AGENTS.md
- General workflow → Ask CTO agent

---

**You're not alone. You have a whole team now.** 🚀

_Remember: These are YOUR agents. They work for YOU. Direct them, learn from them, and build amazing things together._

---

_Quick Start Guide v1.0_  
_Created: 2025-12-27_  
_For: CEO Sean's AI-powered development team_
