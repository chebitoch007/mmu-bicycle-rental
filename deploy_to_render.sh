#!/bin/bash

# Quick Deploy to Render Script
# This prepares your project for Render deployment

echo "🚀 Preparing MMU Bicycle Rental for Render Deployment"
echo "======================================================="
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Initializing git repository..."
    git init
    echo "✅ Git initialized"
else
    echo "✅ Git repository already initialized"
fi

# Make build script executable
echo "🔧 Making build.sh executable..."
chmod +x build.sh
echo "✅ build.sh is now executable"

# Check if .gitignore exists
if [ ! -f .gitignore ]; then
    echo "❌ .gitignore not found! Creating one..."
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
dist/
*.egg-info/

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
/media
/staticfiles

# Environment
.env
.venv
env/
venv/
.DS_Store

# IDEs
.vscode/
.idea/
*.swp
*.swo
EOF
    echo "✅ Created .gitignore"
fi

# Check if remote is set
if git remote | grep -q "origin"; then
    echo "✅ Git remote 'origin' already configured"
else
    echo ""
    echo "⚠️  Git remote not configured"
    echo "📝 After creating your GitHub repository, run:"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/mmu-bicycle-rental.git"
fi

# Stage all files
echo ""
echo "📦 Staging files for commit..."
git add .

# Show status
echo ""
echo "📊 Git status:"
git status --short

# Prompt for commit
echo ""
read -p "📝 Enter commit message (or press Enter for default): " commit_msg
if [ -z "$commit_msg" ]; then
    commit_msg="Prepare for Render deployment"
fi

git commit -m "$commit_msg"
echo "✅ Files committed"

echo ""
echo "======================================================="
echo "✅ Project prepared for deployment!"
echo ""
echo "📋 Next steps:"
echo "   1. Create GitHub repository at https://github.com/new"
echo "   2. Run: git remote add origin https://github.com/YOUR_USERNAME/mmu-bicycle-rental.git"
echo "   3. Run: git push -u origin main"
echo "   4. Go to render.com and create new Web Service"
echo "   5. Connect your GitHub repository"
echo "   6. Configure as shown in DEPLOYMENT_GUIDE.md"
echo ""
echo "🔗 Quick links:"
echo "   - Create GitHub repo: https://github.com/new"
echo "   - Render Dashboard: https://dashboard.render.com"
echo ""
echo "📖 Full guide: See DEPLOYMENT_GUIDE.md"
echo "======================================================="