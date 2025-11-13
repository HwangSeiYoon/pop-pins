# Git 디렉토리별 브랜치 관리 가이드

디렉토리별로 별도의 브랜치를 생성하고 GitHub에 관리하는 방법입니다.

## 방법 1: 하나의 저장소에서 브랜치별로 디렉토리 관리 (권장)

각 디렉토리를 별도의 브랜치에서 관리하되, 하나의 저장소를 사용합니다.

### 1단계: Git 저장소 초기화 (아직 안 했다면)

```bash
cd /Users/hooni/POP.PNIS
git init
```

### 2단계: .gitignore 파일 생성

```bash
cat > .gitignore << EOF
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
```

### 3단계: 메인 브랜치에 초기 커밋

```bash
git add .gitignore
git commit -m "Initial commit: Add .gitignore"
```

### 4단계: 각 디렉토리별 브랜치 생성 및 설정

#### frontend 브랜치 생성

```bash
# frontend 브랜치 생성 및 전환
git checkout -b frontend

# frontend 디렉토리만 추가
git add frontend/
git commit -m "Add frontend directory"

# GitHub에 브랜치 푸시
git push -u origin frontend
```

#### 다른 디렉토리가 있다면 (예: backend)

```bash
# backend 브랜치 생성
git checkout -b backend

# backend 디렉토리만 추가
git add backend/
git commit -m "Add backend directory"

# GitHub에 브랜치 푸시
git push -u origin backend
```

### 5단계: GitHub 저장소 생성 및 연결

```bash
# GitHub에서 새 저장소 생성 후
git remote add origin https://github.com/사용자명/저장소명.git
git branch -M main
git push -u origin main
```

## 방법 2: 각 디렉토리를 별도의 Git 저장소로 분리

각 디렉토리를 완전히 독립적인 Git 저장소로 관리합니다.

### frontend를 별도 저장소로

```bash
cd /Users/hooni/POP.PNIS/frontend

# Git 초기화
git init

# .gitignore 생성
cat > .gitignore << EOF
__pycache__/
*.py[cod]
venv/
env/
EOF

# 파일 추가 및 커밋
git add .
git commit -m "Initial commit: frontend"

# GitHub에 새 저장소 생성 후
git remote add origin https://github.com/사용자명/pop-pnis-frontend.git
git branch -M main
git push -u origin main
```

### 다른 디렉토리도 동일하게

각 디렉토리마다 별도의 GitHub 저장소를 생성하여 관리합니다.

## 방법 3: Git Subtree 사용 (고급)

하나의 저장소에서 각 디렉토리를 독립적으로 관리하면서도 통합할 수 있습니다.

```bash
# frontend를 subtree로 푸시
git subtree push --prefix=frontend origin frontend-subtree
```

## 추천 워크플로우

### 방법 1 사용 시 (브랜치별 관리)

```bash
# frontend 작업 시
git checkout frontend
# ... 작업 ...
git add frontend/
git commit -m "Update frontend"
git push origin frontend

# 다른 디렉토리 작업 시
git checkout main  # 또는 다른 브랜치
# ... 작업 ...
```

### 방법 2 사용 시 (별도 저장소)

```bash
# frontend 작업
cd frontend
git add .
git commit -m "Update"
git push origin main

# 다른 디렉토리 작업
cd ../다른디렉토리
git add .
git commit -m "Update"
git push origin main
```

## 브랜치별로 특정 디렉토리만 추적하기

`.git/info/sparse-checkout` 파일을 사용하여 브랜치별로 특정 디렉토리만 추적할 수 있습니다.

```bash
# frontend 브랜치에서
git checkout frontend
git config core.sparseCheckout true
echo "frontend/*" > .git/info/sparse-checkout
git read-tree -m -u HEAD
```

## 주의사항

1. **방법 1**: 브랜치 간 전환 시 다른 디렉토리도 함께 전환됩니다.
2. **방법 2**: 각 디렉토리가 완전히 독립적이지만, 통합 관리가 어려울 수 있습니다.
3. **방법 3**: 복잡하지만 유연한 관리가 가능합니다.

## 빠른 시작 스크립트

다음 스크립트를 실행하면 자동으로 설정됩니다:

```bash
#!/bin/bash
# setup_git_branches.sh

cd /Users/hooni/POP.PNIS

# Git 초기화 (이미 되어있으면 스킵)
if [ ! -d .git ]; then
    git init
    echo "Git 저장소 초기화 완료"
fi

# .gitignore 생성
cat > .gitignore << 'EOF'
__pycache__/
*.py[cod]
venv/
env/
.vscode/
.DS_Store
data/
EOF

# 메인 브랜치 초기 커밋
git add .gitignore
git commit -m "Initial commit: Add .gitignore" 2>/dev/null || echo "이미 커밋됨"

# frontend 브랜치 생성
git checkout -b frontend 2>/dev/null || git checkout frontend
git add frontend/
git commit -m "Add frontend directory" 2>/dev/null || echo "이미 커밋됨"

echo "✅ frontend 브랜치 생성 완료!"
echo "다음 명령어로 GitHub에 푸시하세요:"
echo "  git remote add origin <GitHub 저장소 URL>"
echo "  git push -u origin frontend"
```

## GitHub 저장소 생성 및 연결

1. GitHub에서 새 저장소 생성
2. 다음 명령어 실행:

```bash
git remote add origin https://github.com/사용자명/저장소명.git
git push -u origin main
git push -u origin frontend
```


