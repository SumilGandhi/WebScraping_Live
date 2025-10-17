# 📝 Git Workflow Guide

## Initial Setup

```bash
# Initialize git repository
git init

# Add all files
git add .

# First commit
git commit -m "Initial commit: Crypto price tracker web scraper"

# Create GitHub repository (on GitHub.com)
# Then connect local to remote
git remote add origin https://github.com/yourusername/flask_web_scraper.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Regular Commit Workflow

### Making Changes
```bash
# Check status
git status

# Add specific files
git add app.py
git add templates/index.html

# Or add all changes
git add .

# Commit with meaningful message
git commit -m "feat: Add cryptocurrency price scraping functionality"

# Push to GitHub
git push origin main
```

## Commit Message Best Practices

### Format
```
<type>: <subject>

<body (optional)>
```

### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **test**: Adding tests
- **chore**: Maintenance tasks

### Examples
```bash
git commit -m "feat: Add CoinGecko API integration for live crypto prices"
git commit -m "feat: Implement news scraping from CoinDesk"
git commit -m "fix: Resolve database connection timeout issues"
git commit -m "style: Update UI with modern gradient design"
git commit -m "docs: Add comprehensive README and deployment guide"
git commit -m "refactor: Optimize scraping function for better performance"
git commit -m "chore: Update dependencies to latest versions"
```

## Recommended Commit Sequence for This Project

```bash
# 1. Initial project structure
git add .
git commit -m "chore: Initialize Flask project structure"
git push origin main

# 2. Database models
git add app.py
git commit -m "feat: Create database models for crypto and news"
git push origin main

# 3. Scraping functionality
git add app.py
git commit -m "feat: Implement crypto price scraping with CoinGecko API"
git push origin main

git commit -m "feat: Add news scraping from CoinDesk"
git push origin main

# 4. Frontend
git add templates/ static/
git commit -m "feat: Design responsive UI for crypto tracker"
git push origin main

# 5. Automation
git add app.py
git commit -m "feat: Add APScheduler for automated data updates"
git push origin main

# 6. API endpoints
git add app.py
git commit -m "feat: Create REST API endpoint for crypto data"
git push origin main

# 7. Documentation
git add README.md DEPLOYMENT.md
git commit -m "docs: Add comprehensive documentation and deployment guide"
git push origin main

# 8. Deployment files
git add Procfile runtime.txt Dockerfile
git commit -m "chore: Add deployment configuration files"
git push origin main

# 9. Final touches
git add .
git commit -m "style: Polish UI and add loading animations"
git push origin main
```

## Branch Strategy (For Team Projects)

```bash
# Create feature branch
git checkout -b feature/add-portfolio-tracking

# Make changes and commit
git add .
git commit -m "feat: Add portfolio tracking feature"

# Push feature branch
git push origin feature/add-portfolio-tracking

# Create Pull Request on GitHub
# After review and merge, switch back to main
git checkout main
git pull origin main

# Delete feature branch
git branch -d feature/add-portfolio-tracking
```

## Useful Git Commands

```bash
# View commit history
git log --oneline --graph --all

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard all local changes
git reset --hard HEAD

# View changes before committing
git diff

# View changes of specific file
git diff app.py

# Add only part of a file
git add -p app.py

# Create and switch to new branch
git checkout -b feature-name

# Switch branches
git checkout main

# Pull latest changes
git pull origin main

# View remote repositories
git remote -v

# Check branch
git branch
```

## .gitignore Important

Make sure `.gitignore` excludes:
- `__pycache__/` - Python cache
- `venv/` - Virtual environment
- `instance/*.db` - Database files
- `.env` - Environment variables
- `*.log` - Log files

## GitHub Repository Setup

### 1. Create Repository on GitHub
1. Go to github.com
2. Click "New Repository"
3. Name: `flask-crypto-scraper`
4. Description: "Live cryptocurrency price tracker with web scraping"
5. Public/Private
6. Don't initialize with README (you already have one)

### 2. Add Repository Topics
On GitHub repository page, add topics:
- `flask`
- `web-scraping`
- `cryptocurrency`
- `python`
- `sqlalchemy`
- `beautifulsoup`
- `rest-api`

### 3. Add Repository Description
"Dynamic web scraper that fetches live cryptocurrency prices and news. Built with Flask, SQLAlchemy, and BeautifulSoup. Features automated updates and REST API."

## Common Issues

### Large files
```bash
# Remove file from git but keep locally
git rm --cached large_file.db
echo "large_file.db" >> .gitignore
git commit -m "chore: Remove large database file from tracking"
```

### Wrong commit message
```bash
# Amend last commit message
git commit --amend -m "fix: Correct commit message"
git push --force origin main  # Use with caution!
```

### Merge conflicts
```bash
# Pull latest changes
git pull origin main

# If conflicts, edit files to resolve
# Then:
git add .
git commit -m "merge: Resolve conflicts"
git push origin main
```

## Deployment with Git

### Heroku
```bash
heroku login
heroku create
git push heroku main
```

### Railway
- Connect GitHub repo
- Auto-deploys on push to main

### Render
- Connect GitHub repo
- Choose branch: main
- Auto-deploys on push

---

💡 **Pro Tip**: Commit early, commit often, and always write meaningful commit messages!
