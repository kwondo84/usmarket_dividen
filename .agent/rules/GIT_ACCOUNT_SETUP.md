# Git 계정별 구분 설정 가이드

여러 GitHub 계정을 프로젝트별로 구분해서 사용하는 방법입니다.

## 📋 개요

- **kwondo84**: 이 저장소 (AI 배당솔루션)
- **ipnow2025**: 다른 저장소에서 사용

## 🔧 설정 방법

### 1. 현재 저장소에 특정 계정 설정 (로컬 설정)

특정 프로젝트에서만 특정 계정을 사용하려면:

```bash
# 저장소로 이동
cd /path/to/your/project

# 계정 정보 설정
git config user.name "kwondo84"
git config user.email "kwondo84@users.noreply.github.com"

# 또는 ipnow2025로 설정
git config user.name "ipnow2025"
git config user.email "ipnow2025@users.noreply.github.com"
```

### 2. 설정 확인

```bash
# 현재 저장소의 설정 확인
git config user.name
git config user.email

# 모든 설정 확인
git config --list | grep -E "(user|remote)"
```

### 3. 원격 저장소 URL 설정

#### 방법 A: SSH 사용 (권장)

```bash
# SSH 키 확인
ls -la ~/.ssh/id_*.pub

# 원격 저장소 URL을 SSH 형식으로 변경
git remote set-url origin git@github.com:USERNAME/REPO_NAME.git

# 예시
git remote set-url origin git@github.com:kwondo84/usmarket_dividen.git
```

#### 방법 B: HTTPS + Personal Access Token

```bash
# Personal Access Token 생성 필요
# GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)

# URL에 토큰 포함
git remote set-url origin https://YOUR_TOKEN@github.com/USERNAME/REPO_NAME.git
```

### 4. 원격 저장소 확인

```bash
git remote -v
```

## 📝 계정 구분 전략

### 전략 1: 프로젝트별 로컬 설정 (권장)

각 프로젝트마다 다른 계정을 사용하는 경우:

```bash
# 프로젝트 A (kwondo84)
cd /path/to/project-a
git config user.name "kwondo84"
git config user.email "kwondo84@users.noreply.github.com"

# 프로젝트 B (ipnow2025)
cd /path/to/project-b
git config user.name "ipnow2025"
git config user.email "ipnow2025@users.noreply.github.com"
```

### 전략 2: 전역 + 로컬 오버라이드

기본값을 하나로 설정하고, 특정 프로젝트만 다른 계정 사용:

```bash
# 전역 설정 (기본값: ipnow2025)
git config --global user.name "ipnow2025"
git config --global user.email "ipnow2025@users.noreply.github.com"

# 특정 프로젝트만 다른 계정 사용 (kwondo84)
cd /path/to/specific-project
git config user.name "kwondo84"
git config user.email "kwondo84@users.noreply.github.com"
```

## 🚀 커밋 및 Push

### 커밋 전 확인

```bash
# 상태 확인
git status

# 변경사항 확인
git diff

# 커밋 이력 확인
git log --oneline -5
```

### 커밋 및 Push

```bash
# 변경사항 스테이징
git add .

# 커밋
git commit -m "커밋 메시지"

# Push (SSH 사용 시)
git push -u origin main

# Push (HTTPS + Token 사용 시)
git push -u origin main
# → 토큰 입력 요청 시 Personal Access Token 입력
```

## 🔍 문제 해결

### 인증 오류

**문제**: `Authentication failed` 또는 `Invalid username or token`

**해결**:
1. SSH 키 사용 (권장)
   ```bash
   git remote set-url origin git@github.com:USERNAME/REPO_NAME.git
   ```

2. Personal Access Token 생성 및 사용
   - GitHub → Settings → Developer settings → Personal access tokens
   - `repo` 권한 선택
   - 생성된 토큰으로 URL 업데이트

### 설정이 적용되지 않음

**확인**:
```bash
# 로컬 설정 확인
git config user.name
git config user.email

# 전역 설정 확인
git config --global user.name
git config --global user.email
```

**해결**: 로컬 설정이 전역 설정보다 우선순위가 높습니다. 로컬 설정이 없으면 전역 설정이 사용됩니다.

### 권한 오류

**문제**: `Operation not permitted` 또는 `could not write config file`

**해결**: 
- 파일 권한 확인
- 필요시 `required_permissions: ['all']` 사용 (개발 환경에서)

## 📌 현재 프로젝트 설정

### AI 배당솔루션 프로젝트

```bash
# 저장소 위치
/Users/kwondohun/Documents/⭐️권도훈/dev/AI 배당솔루션

# 계정 설정
user.name=kwondo84
user.email=kwondo84@users.noreply.github.com

# 원격 저장소
origin: git@github.com:kwondo84/usmarket_dividen.git
```

## 💡 팁

1. **SSH 키 사용 권장**: Personal Access Token보다 안전하고 편리합니다.
2. **계정별 이메일**: GitHub의 `username@users.noreply.github.com` 형식 사용 권장
3. **설정 확인**: 커밋 전에 항상 `git config user.name`으로 확인
4. **일관성 유지**: 프로젝트별로 일관된 계정 사용

## 🔗 참고 링크

- [GitHub Personal Access Tokens](https://github.com/settings/tokens)
- [Git Config 문서](https://git-scm.com/docs/git-config)
- [SSH 키 생성 및 추가](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
