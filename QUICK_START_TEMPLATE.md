# Quick Start: AI Agent Template
## Copy & Paste Commands for Your Next Project

---

## 🚀 Setup New Project (3 Commands)

```bash
# 1. Navigate to your new project
cd /Users/Sean/code/YOUR-PROJECT-NAME

# 2. Copy the init script
cp /Users/Sean/code/gutter-tracker/init-ai-docs.sh .

# 3. Run it with your project details
./init-ai-docs.sh "YOUR-PROJECT-NAME" "YOUR-TECH-STACK"
```

**Example:**
```bash
cd /Users/Sean/code/my-django-blog
cp /Users/Sean/code/gutter-tracker/init-ai-docs.sh .
./init-ai-docs.sh "my-django-blog" "Python/Django"
```

---

## 📚 Common Tech Stacks

Copy/paste the one you need:

### Python Projects
```bash
./init-ai-docs.sh "my-project" "Python/Flask"
./init-ai-docs.sh "my-project" "Python/Django"
./init-ai-docs.sh "my-project" "Python/FastAPI"
./init-ai-docs.sh "my-project" "Python/Streamlit"
```

### JavaScript Projects
```bash
./init-ai-docs.sh "my-project" "Node.js/Express"
./init-ai-docs.sh "my-project" "React"
./init-ai-docs.sh "my-project" "Next.js"
./init-ai-docs.sh "my-project" "Vue.js"
```

### Other Stacks
```bash
./init-ai-docs.sh "my-project" "Ruby/Rails"
./init-ai-docs.sh "my-project" "Go/Gin"
./init-ai-docs.sh "my-project" "Rust/Actix"
./init-ai-docs.sh "my-project" "Java/Spring"
```

---

## ✅ After Running Script

```bash
# 1. Customize the generated files
# Edit AGENTS.md, CLAUDE.md, GEMINI.md, etc.

# 2. Add to git
git add AGENTS.md CLAUDE.md GEMINI.md TROUBLESHOOTING.md CLEANUP.md init-ai-docs.sh

# 3. Commit
git commit -m "Add AI agent documentation suite"
```

---

## 🎯 Quick Setup: Apply to All Projects

### One-Time Setup (Create Master Template)
```bash
# Create template directory
mkdir -p /Users/Sean/code/.templates/ai-agent-docs

# Copy files there
cp /Users/Sean/code/gutter-tracker/init-ai-docs.sh /Users/Sean/code/.templates/ai-agent-docs/
cp /Users/Sean/code/gutter-tracker/AI_AGENT_WORKFLOW_TEMPLATE.md /Users/Sean/code/.templates/ai-agent-docs/
cp /Users/Sean/code/gutter-tracker/HOW_TO_USE_TEMPLATE.md /Users/Sean/code/.templates/ai-agent-docs/

# Make executable
chmod +x /Users/Sean/code/.templates/ai-agent-docs/init-ai-docs.sh

# Add alias to shell (zsh)
echo 'alias init-ai-docs="/Users/Sean/code/.templates/ai-agent-docs/init-ai-docs.sh"' >> ~/.zshrc
source ~/.zshrc
```

### Now Use From Anywhere
```bash
# Go to any project
cd /Users/Sean/code/any-project

# Run the command
init-ai-docs "project-name" "tech-stack"

# Done!
```

---

## 📋 What Gets Created

After running the script, you'll have:

```
your-project/
├── AGENTS.md              ✅ Main dev guide (customize this!)
├── CLAUDE.md              ✅ Claude CLI context
├── GEMINI.md              ✅ Gemini context
├── TROUBLESHOOTING.md     ✅ Common issues
├── CLEANUP.md             ✅ Disk maintenance
└── init-ai-docs.sh        ✅ Script (for others)
```

---

## 🤖 Using With AI Agents

### First Session with Claude
```
You: "I have a Python project. Read AGENTS.md for context."
Claude: [Reads file, has full context]
You: "Let's add user authentication"
Claude: [Works with full project knowledge]
```

### Switching to Gemini
```
You: "Read AGENTS.md and GEMINI.md. What did we build?"
Gemini: [Catches up from docs]
You: "Now add password reset feature"
Gemini: [Continues seamlessly]
```

---

## 💡 Customization Tips

### Must Customize (Do First)
1. **AGENTS.md** → Update project name, tech stack, commands
2. **AGENTS.md** → Add your actual file structure
3. **AGENTS.md** → Update production URL/platform if deployed

### Can Customize Later
1. **TROUBLESHOOTING.md** → Add issues as you encounter them
2. **CLAUDE.md** → Add common patterns you develop
3. **GEMINI.md** → Add AI features if using Gemini API

### Rarely Need to Touch
1. **CLEANUP.md** → Generic cleanup commands work for most projects

---

## 🔍 Examples: Real Projects

### Example 1: Personal Blog (Django)
```bash
cd ~/code/my-blog
cp ~/code/gutter-tracker/init-ai-docs.sh .
./init-ai-docs.sh "my-blog" "Python/Django"

# Edit AGENTS.md:
# - Update commands: python manage.py runserver, etc.
# - Add: Blog models, template structure
# - Production: Where it's deployed

git add *.md init-ai-docs.sh
git commit -m "Add AI agent docs"
```

### Example 2: API Service (FastAPI)
```bash
cd ~/code/api-service
cp ~/code/gutter-tracker/init-ai-docs.sh .
./init-ai-docs.sh "api-service" "Python/FastAPI"

# Edit AGENTS.md:
# - Update commands: uvicorn main:app --reload
# - Add: API endpoints, database models
# - Add: Authentication scheme

git add *.md init-ai-docs.sh
git commit -m "Add AI agent docs"
```

### Example 3: React App (Next.js)
```bash
cd ~/code/my-react-app
cp ~/code/gutter-tracker/init-ai-docs.sh .
./init-ai-docs.sh "my-react-app" "Next.js"

# Edit AGENTS.md:
# - Update commands: npm run dev, npm test
# - Change structure: src/, components/, pages/
# - Add: Component library, state management

git add *.md init-ai-docs.sh
git commit -m "Add AI agent docs"
```

---

## ⚡ Super Quick Reference

| Task | Command |
|------|---------|
| **Setup new project** | `init-ai-docs "name" "stack"` |
| **Check what was created** | `ls *.md` |
| **Customize main doc** | Edit `AGENTS.md` |
| **Commit to git** | `git add *.md && git commit -m "Add AI docs"` |
| **Use with Claude** | "Read AGENTS.md for context" |

---

## 📖 Full Documentation

For complete details, see:
- **AI_AGENT_WORKFLOW_TEMPLATE.md** - Complete template reference
- **HOW_TO_USE_TEMPLATE.md** - Comprehensive usage guide
- **gutter-tracker/AGENTS.md** - Real-world example

---

## 🎉 That's It!

You now have a reusable template for ALL your projects.

**Next:** Apply it to your other projects in `/Users/Sean/code/`

Good luck! 🚀
