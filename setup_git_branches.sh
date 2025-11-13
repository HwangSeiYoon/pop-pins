#!/bin/bash
# Git 디렉토리별 브랜치 설정 스크립트

cd /Users/hooni/POP.PNIS

echo "🚀 Git 브랜치 설정을 시작합니다..."
echo ""

# Git 초기화 확인
if [ ! -d .git ]; then
    echo "📦 Git 저장소 초기화 중..."
    git init
    echo "✅ Git 저장소 초기화 완료"
else
    echo "✅ Git 저장소가 이미 존재합니다"
fi

# .gitignore 생성
echo ""
echo "📝 .gitignore 파일 생성 중..."
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Data
data/
*.json.bak
EOF
echo "✅ .gitignore 생성 완료"

# 메인 브랜치 초기 커밋
echo ""
echo "📌 메인 브랜치 설정 중..."
git add .gitignore pyrightconfig.json 2>/dev/null
if git diff --staged --quiet 2>/dev/null; then
    echo "ℹ️  변경사항이 없습니다"
else
    git commit -m "Initial commit: Add .gitignore and config files" 2>/dev/null
    echo "✅ 메인 브랜치 초기 커밋 완료"
fi

# frontend 브랜치 생성
echo ""
echo "🌿 frontend 브랜치 생성 중..."
if git show-ref --verify --quiet refs/heads/frontend; then
    echo "ℹ️  frontend 브랜치가 이미 존재합니다"
    git checkout frontend
else
    git checkout -b frontend
    echo "✅ frontend 브랜치 생성 완료"
fi

# frontend 디렉토리 추가
echo ""
echo "📁 frontend 디렉토리 추가 중..."
git add frontend/ 2>/dev/null
if git diff --staged --quiet 2>/dev/null; then
    echo "ℹ️  frontend 디렉토리가 이미 커밋되어 있습니다"
else
    git commit -m "Add frontend directory with FastAPI backend and HTML views"
    echo "✅ frontend 디렉토리 커밋 완료"
fi

echo ""
echo "=" * 50
echo "✅ 설정 완료!"
echo "=" * 50
echo ""
echo "다음 단계:"
echo "1. GitHub에서 새 저장소를 생성하세요"
echo "2. 다음 명령어를 실행하세요:"
echo ""
echo "   git remote add origin https://github.com/사용자명/저장소명.git"
echo "   git checkout main"
echo "   git push -u origin main"
echo "   git checkout frontend"
echo "   git push -u origin frontend"
echo ""
echo "현재 브랜치: $(git branch --show-current)"
echo "브랜치 목록:"
git branch


