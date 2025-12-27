# How to Use the AI Agent Workflow Template
## Complete Guide for Multi-Project Setup

This guide shows you how to replicate the AI agent documentation setup from `gutter-tracker` to ALL your other projects.

---

## 🎯 What This Template Does

Creates a **complete AI agent documentation suite** for any project so that:
- ✅ Claude, Gemini, Cursor, and other AI CLIs have full context
- ✅ Any agent can pick up where another left off
- ✅ You get consistent, high-quality assistance across all projects
- ✅ No more repeating context every session

---

## 📦 Files Included

### Core Documentation
1. **AI_AGENT_WORKFLOW_TEMPLATE.md** - This template (you're reading it!)
2. **init-ai-docs.sh** - Auto-generates all docs for new projects
3. **HOW_TO_USE_TEMPLATE.md** - This guide

### Generated Documentation (created by script)
1. **AGENTS.md** - Main development guide (read first)
2. **CLAUDE.md** - Claude-specific context
3. **GEMINI.md** - Gemini-specific context  
4. **TROUBLESHOOTING.md** - Common issues & solutions
5. **CLEANUP.md** - Disk space & maintenance

---

## 🚀 Quick Start: New Project Setup

### Option 1: Using the Script (Recommended)

```bash
# Navigate to your NEW project
cd /Users/Sean/code/my-new-project

# Copy the init script from gutter-tracker
cp /Users/Sean/code/gutter-tracker/init-ai-docs.sh .

# Run it with your project details
./init-ai-docs.sh "my-new-project" "Python/Django"

# Customize the generated files
# Edit AGENTS.md, CLAUDE.md, etc. with your project specifics

# Commit to git
git add AGENTS.md CLAUDE.md GEMINI.md TROUBLESHOOTING.md CLEANUP.md init-ai-docs.sh
git commit -m "Add AI agent documentation suite"
```

### Option 2: Manual Setup

```bash
# Navigate to your project
cd /Users/Sean/code/my-new-project

# Copy all template files
cp /Users/Sean/code/gutter-tracker/AGENTS.md .
cp /Users/Sean/code/gutter-tracker/CLAUDE.md .
cp /Users/Sean/code/gutter-tracker/GEMINI.md .
cp /Users/Sean/code/gutter-tracker/TROUBLESHOOTING.md .
cp /Users/Sean/code/gutter-tracker/CLEANUP.md .

# Edit each file to match your project
# Replace project name, tech stack, commands, etc.

# Commit
git add *.md
git commit -m "Add AI agent documentation"
```

---

## 📝 Customization Checklist

After generating docs, customize these sections:

### In AGENTS.md
- [ ] Project name and description
- [ ] Tech stack details
- [ ] Quick start commands (update `make` commands)
- [ ] Project structure (match your folders)
- [ ] Environment variables (your specific vars)
- [ ] Production URL and platform
- [ ] Testing commands (your test framework)

### In CLAUDE.md  
- [ ] Project context (what it does)
- [ ] Common patterns (your coding patterns)
- [ ] User preferences (your coding style)
- [ ] Emergency contacts (where to check logs)

### In GEMINI.md
- [ ] AI integration points (if using Gemini API)
- [ ] Environment setup (your API keys)
- [ ] Gemini-specific features (if any)

### In TROUBLESHOOTING.md
- [ ] Add project-specific issues you've encountered
- [ ] Update diagnostic commands for your stack
- [ ] Add your deployment platform commands
- [ ] Customize emergency procedures

### In CLEANUP.md
- [ ] Update disk usage estimates for your project
- [ ] Add project-specific cleanup commands
- [ ] Adjust backup procedures

---

## 🎨 Template for Different Tech Stacks

### Python/Flask (already included)
```bash
./init-ai-docs.sh "my-flask-app" "Python/Flask"
```

### Python/Django
```bash
./init-ai-docs.sh "my-django-app" "Python/Django"

# Then update AGENTS.md with Django-specific commands:
# python manage.py runserver
# python manage.py test
# python manage.py migrate
```

### Node.js/Express
```bash
./init-ai-docs.sh "my-express-app" "Node.js/Express"

# Update AGENTS.md:
# npm install
# npm run dev
# npm test
# npm run build
```

### React/Next.js
```bash
./init-ai-docs.sh "my-nextjs-app" "React/Next.js"

# Update AGENTS.md:
# npm install
# npm run dev
# npm run build
# npm test
```

### Python/FastAPI
```bash
./init-ai-docs.sh "my-fastapi-app" "Python/FastAPI"

# Update AGENTS.md:
# uvicorn main:app --reload
# pytest
# pip install -r requirements.txt
```

---

## 🔄 Using Across Multiple Projects

### Step 1: Create Master Template Directory
```bash
# Create a central template location
mkdir -p /Users/Sean/code/.templates/ai-agent-docs

# Copy the init script there
cp /Users/Sean/code/gutter-tracker/init-ai-docs.sh /Users/Sean/code/.templates/ai-agent-docs/
cp /Users/Sean/code/gutter-tracker/AI_AGENT_WORKFLOW_TEMPLATE.md /Users/Sean/code/.templates/ai-agent-docs/
cp /Users/Sean/code/gutter-tracker/HOW_TO_USE_TEMPLATE.md /Users/Sean/code/.templates/ai-agent-docs/

# Make it executable
chmod +x /Users/Sean/code/.templates/ai-agent-docs/init-ai-docs.sh
```

### Step 2: Add Alias to Shell Config
```bash
# Add to ~/.zshrc or ~/.bashrc
echo 'alias init-ai-docs="/Users/Sean/code/.templates/ai-agent-docs/init-ai-docs.sh"' >> ~/.zshrc

# Reload shell
source ~/.zshrc

# Now you can use it from anywhere
cd /Users/Sean/code/any-project
init-ai-docs "project-name" "tech-stack"
```

### Step 3: Apply to Existing Projects
```bash
# For each existing project in /Users/Sean/code/
cd /Users/Sean/code/project-1
init-ai-docs "project-1" "Python/Flask"

cd /Users/Sean/code/project-2
init-ai-docs "project-2" "Node.js/React"

cd /Users/Sean/code/project-3
init-ai-docs "project-3" "Python/Django"

# etc...
```

---

## 🤖 AI Agent Usage Patterns

### First Session with New Project
When starting work with an AI agent on a new project:

```
You: "I have a project called X. Read AGENTS.md for context."
AI: [Reads AGENTS.md, understands project]
You: "Let's add feature Y"
AI: [Has all context, works efficiently]
```

### Switching Between Agents
```
Claude Session 1:
You: "Add login feature"
Claude: [Adds login, updates AGENTS.md]

Gemini Session 2:
You: "Read AGENTS.md. What did we do last?"
Gemini: [Reads AGENTS.md, sees login was added]
You: "Now add password reset"
Gemini: [Continues seamlessly]
```

### Reporting Issues
```
You: "The app is crashing on startup"
Claude: [Checks TROUBLESHOOTING.md first]
Claude: "Found similar issue in TROUBLESHOOTING.md section 1. Trying solution..."
```

---

## 📊 Example Directory Structure After Setup

```
/Users/Sean/code/
├── .templates/
│   └── ai-agent-docs/
│       ├── init-ai-docs.sh
│       ├── AI_AGENT_WORKFLOW_TEMPLATE.md
│       └── HOW_TO_USE_TEMPLATE.md
│
├── gutter-tracker/          # Reference project
│   ├── AGENTS.md            ✅ Complete
│   ├── CLAUDE.md            ✅ Complete
│   ├── GEMINI.md            ✅ Complete
│   ├── TROUBLESHOOTING.md   ✅ Complete
│   ├── CLEANUP.md           ✅ Complete
│   ├── app/
│   └── tests/
│
├── project-1/               # New project with docs
│   ├── AGENTS.md            ✅ Generated
│   ├── CLAUDE.md            ✅ Generated
│   ├── GEMINI.md            ✅ Generated
│   ├── TROUBLESHOOTING.md   ✅ Generated
│   ├── CLEANUP.md           ✅ Generated
│   └── src/
│
├── project-2/               # Another project with docs
│   ├── AGENTS.md            ✅ Generated
│   ├── CLAUDE.md            ✅ Generated
│   └── ...
│
└── project-3/               # And another...
    ├── AGENTS.md            ✅ Generated
    └── ...
```

---

## 💡 Best Practices

### 1. Update Documentation as You Go
```bash
# After making significant changes
# Update AGENTS.md with new patterns/commands
# Update TROUBLESHOOTING.md when you fix new issues
# Commit changes

git add AGENTS.md TROUBLESHOOTING.md
git commit -m "Update AI agent docs with latest patterns"
```

### 2. Keep Documentation in Sync
```bash
# When you change project structure
# Update AGENTS.md immediately

# When you add new dependencies
# Update AGENTS.md Quick Start section

# When you fix a tricky bug
# Add to TROUBLESHOOTING.md
```

### 3. Share Learnings Across Projects
```bash
# Found a useful pattern in project-1?
# Add it to project-2's AGENTS.md
# Keep templates updated

# Example: Great testing pattern
# Add to all projects' AGENTS.md
```

### 4. Version Control
```bash
# Always commit AI docs with code
git add AGENTS.md CLAUDE.md GEMINI.md TROUBLESHOOTING.md CLEANUP.md
git commit -m "Add AI agent documentation"

# Update when project evolves
git add AGENTS.md
git commit -m "Update AGENTS.md with new deployment process"
```

---

## 🎯 Real-World Examples

### Example 1: Starting a New Flask API
```bash
cd ~/code/new-flask-api
init-ai-docs "flask-api" "Python/Flask"

# Customize AGENTS.md
# Add: REST API endpoints, database models, API authentication

# Start coding with Claude
claude code

You: "Read AGENTS.md. Let's build user registration endpoint"
Claude: [Has context, builds correctly]
```

### Example 2: Joining an Existing Team Project
```bash
cd ~/code/team-project

# Your teammate hasn't added AI docs yet
init-ai-docs "team-project" "Node.js/Express"

# Fill in AGENTS.md with what you learn
# Share with team
git push origin add-ai-docs

# Now anyone can use AI agents effectively
```

### Example 3: Multiple AI Agents on Same Project
```bash
# Morning: Use Claude for features
claude code
You: "Read AGENTS.md. Add dark mode toggle"

# Afternoon: Use Gemini for creative work
gemini code
You: "Read AGENTS.md. Design a better homepage layout"

# Evening: Use Cursor for refactoring
cursor
You: [Cursor reads AGENTS.md automatically]
You: "Refactor auth system"

# All agents have same context, work seamlessly
```

---

## 🔧 Advanced: Custom Agent Files

### Adding Cursor-Specific Context
```bash
# Create CURSOR.md
cat > CURSOR.md << 'EOF'
# CURSOR.md - Cursor IDE Context

## Cursor-Specific Features
- Uses inline AI assistance
- Can see full file context
- Great for refactoring

## Quick Actions
- Cmd+K: Inline edit
- Cmd+L: Chat with context
- Cmd+I: Generate code

## Preferred by User For
- Large refactors
- UI/UX improvements
- Code review

See AGENTS.md for full project context.
EOF
```

### Adding Copilot-Specific Context
```bash
# Create COPILOT.md
cat > COPILOT.md << 'EOF'
# COPILOT.md - GitHub Copilot Context

## Copilot-Specific Patterns
- Use descriptive comments for better suggestions
- Follow established code patterns

## Project Conventions
[Your coding conventions]

See AGENTS.md for full project context.
EOF
```

---

## 📚 Reference: Complete Template File Structure

```
project/
├── AGENTS.md              # Main guide (read first)
├── CLAUDE.md              # Claude CLI context
├── GEMINI.md              # Gemini context
├── CURSOR.md              # (optional) Cursor IDE
├── COPILOT.md             # (optional) GitHub Copilot
├── TROUBLESHOOTING.md     # Common issues
├── CLEANUP.md             # Disk maintenance
├── init-ai-docs.sh        # Generator script
└── .clinerules            # (optional) Project rules
```

---

## ✅ Success Checklist

After setting up AI docs for a project:

- [ ] All 5 core .md files created (AGENTS, CLAUDE, GEMINI, TROUBLESHOOTING, CLEANUP)
- [ ] Project-specific details filled in (not just templates)
- [ ] Quick start commands tested and verified
- [ ] Production details documented (if deployed)
- [ ] Common issues added to TROUBLESHOOTING.md
- [ ] All files committed to git
- [ ] Tested with at least one AI agent (verify it has context)

---

## 🎓 Learning from gutter-tracker

The `gutter-tracker` project is your **reference implementation**. When customizing for new projects:

1. **Look at gutter-tracker's AGENTS.md** - See how it's structured
2. **Check TROUBLESHOOTING.md** - See real issues and solutions
3. **Review CLAUDE.md** - See what context Claude needs
4. **Use CLEANUP.md** - See maintenance patterns

Copy the **structure and style**, but customize the **content** for each project.

---

## 🚨 Common Mistakes to Avoid

### ❌ Don't Do This
```bash
# Copying files without customization
cp gutter-tracker/AGENTS.md new-project/AGENTS.md  # Wrong!
# The new project will have gutter-tracker details
```

### ✅ Do This Instead
```bash
# Generate fresh docs, then customize
cd new-project
init-ai-docs "new-project" "Python/FastAPI"
# Then edit each file with project-specific details
```

### ❌ Don't Do This
```bash
# Creating docs once and never updating
# [6 months later, docs are outdated and useless]
```

### ✅ Do This Instead
```bash
# Update docs whenever project changes significantly
git add AGENTS.md
git commit -m "Update AGENTS.md with new Docker deployment process"
```

---

## 💬 Questions & Answers

### Q: Do I need all 5 documentation files?
**A:** Minimum: AGENTS.md and TROUBLESHOOTING.md. Recommended: All 5.

### Q: Can I use this for non-Python projects?
**A:** Yes! Just update the tech stack and commands. Works for any language.

### Q: How often should I update the docs?
**A:** Update AGENTS.md when project structure changes. Update TROUBLESHOOTING.md when you fix new issues. Update weekly is good practice.

### Q: What if my team doesn't use AI agents?
**A:** The docs still help! They serve as living project documentation for any developer.

### Q: Can I share this template with others?
**A:** Yes! Share the init-ai-docs.sh script and this guide. Help others get better AI assistance.

---

## 🎉 Next Steps

1. **Create master template directory** (see "Using Across Multiple Projects")
2. **Apply to one existing project** (test the workflow)
3. **Refine based on your experience**
4. **Apply to all other projects**
5. **Share with team/community**

---

## 📞 Support

If you run into issues:
1. Check the gutter-tracker project as reference
2. Review this guide's examples
3. Test the init-ai-docs.sh script in a test project first
4. Ask your AI agent for help (they can read this guide!)

---

**Made with ❤️ based on the gutter-tracker project workflow**
**Last updated: 2025-12-27**
