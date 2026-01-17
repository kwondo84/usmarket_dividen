# Git 계정 설정 빠른 참조

## 🚀 빠른 설정 (3단계)

### 1단계: 계정 정보 설정
```bash
cd /path/to/your/project
git config user.name "계정명"
git config user.email "계정명@users.noreply.github.com"
```

### 2단계: 원격 저장소 URL 설정 (SSH)
```bash
git remote set-url origin git@github.com:계정명/저장소명.git
```

### 3단계: 확인 및 Push
```bash
git config user.name  # 설정 확인
git remote -v         # 원격 저장소 확인
git push -u origin main
```

## 📋 계정별 설정 예시

### kwondo84 계정
```bash
git config user.name "kwondo84"
git config user.email "kwondo84@users.noreply.github.com"
git remote set-url origin git@github.com:kwondo84/REPO_NAME.git
```

### ipnow2025 계정
```bash
git config user.name "ipnow2025"
git config user.email "ipnow2025@users.noreply.github.com"
git remote set-url origin git@github.com:ipnow2025/REPO_NAME.git
```

## ✅ 체크리스트

- [ ] 프로젝트 디렉토리로 이동
- [ ] `git config user.name` 설정
- [ ] `git config user.email` 설정
- [ ] `git remote set-url` SSH 형식으로 변경
- [ ] `git config user.name` 확인
- [ ] `git remote -v` 확인
- [ ] 커밋 및 Push 테스트

## 🔍 문제 해결

| 문제 | 해결 방법 |
|------|----------|
| 인증 실패 | SSH로 변경: `git remote set-url origin git@github.com:USER/REPO.git` |
| 설정 안 됨 | `git config user.name` 확인, 로컬 설정 우선 |
| 권한 오류 | 파일 권한 확인 또는 `required_permissions: ['all']` 사용 |

## 💡 핵심 명령어

```bash
# 설정 확인
git config user.name
git config user.email
git remote -v

# 설정 변경
git config user.name "계정명"
git config user.email "계정명@users.noreply.github.com"
git remote set-url origin git@github.com:계정명/저장소명.git

# 커밋 및 Push
git add .
git commit -m "메시지"
git push -u origin main
```
