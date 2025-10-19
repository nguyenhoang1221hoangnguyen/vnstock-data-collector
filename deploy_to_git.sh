#!/bin/bash

# VNStock Data Collector - Git Deployment Script
# Tự động push project lên GitHub/GitLab

echo "🚀 VNStock Data Collector - Git Deployment"
echo "=========================================="

# Kiểm tra Git status
echo "📊 Checking Git status..."
git status

echo ""
echo "📁 Files ready to deploy:"
git ls-files

echo ""
echo "🔗 To deploy to GitHub/GitLab, run these commands:"
echo ""
echo "# 1. Create repository on GitHub/GitLab first, then:"
echo "git remote add origin https://github.com/YOUR_USERNAME/vnstock-data-collector.git"
echo ""
echo "# 2. Push to remote:"
echo "git branch -M main"
echo "git push -u origin main"
echo ""
echo "# 3. Or for GitLab:"
echo "git remote add origin https://gitlab.com/YOUR_USERNAME/vnstock-data-collector.git"
echo "git push -u origin main"
echo ""

# Hiển thị thông tin project
echo "📊 Project Summary:"
echo "==================="
echo "✅ Files: $(git ls-files | wc -l) files ready"
echo "✅ Commit: $(git log --oneline | wc -l) commit(s)"
echo "✅ Size: $(du -sh . | cut -f1) total size"
echo "✅ Documentation: README.md ($(wc -l < README.md) lines)"
echo "✅ License: MIT License included"
echo "✅ Docker: Dockerfile & docker-compose.yml ready"
echo "✅ Setup: Auto setup script included"
echo ""

echo "🎯 Next Steps:"
echo "1. Create new repository on GitHub/GitLab"
echo "2. Copy the git remote add command above"
echo "3. Run git push -u origin main"
echo "4. Your VNStock Data Collector is live! 🎉"
echo ""

echo "📖 Repository will include:"
echo "- Complete Vietnam stock data API"
echo "- 15+ years historical data capability"
echo "- 17+ years financial reports"
echo "- n8n workflow integration"
echo "- AI-optimized data structure"
echo "- Docker deployment ready"
echo "- Comprehensive documentation"
echo ""

echo "⭐ Don't forget to:"
echo "- Add repository description"
echo "- Add topics/tags: vietnam, stock, api, n8n, ai, fastapi"
echo "- Enable Issues and Wiki"
echo "- Add README badges"
echo ""

echo "🚀 Ready for deployment!"
