# TestSprite MCP 설정 UI 문제 - 빠른 해결 방법

## 🚨 핵심 문제

MCP 서버 프로세스는 실행 중이지만, Cursor IDE가 MCP 서버를 인식하지 못하고 있습니다.

**증상**:
- ✅ MCP 서버 프로세스 실행 중
- ❌ `list_mcp_resources`에서 리소스 없음
- ❌ 설정 UI가 나타나지 않음
- ❌ `ide_state.json`의 MCP 섹션이 비어있음

---

## ⚡ 즉시 시도할 수 있는 해결 방법

### 방법 1: Cursor IDE 완전 재시작 (가장 효과적)

1. **모든 Cursor 창 닫기**
2. **프로세스 완전 종료**:
```bash
# macOS에서
killall "Cursor" 2>/dev/null
killall "Cursor Helper" 2>/dev/null

# 또는 Activity Monitor에서 Cursor 프로세스 모두 종료
```

3. **5초 대기**
4. **Cursor IDE 다시 시작**
5. **프로젝트 폴더 열기**
6. **MCP 패널 확인** (사이드바 또는 하단)

### 방법 2: MCP 서버 강제 재시작

```bash
# 실행 중인 MCP 서버 프로세스 종료
pkill -f "testsprite-mcp"

# Cursor IDE 재시작 (위 방법 1 참조)
```

### 방법 3: MCP 설정 파일 재검증 및 수정

현재 설정 파일을 백업하고 다시 작성:

```bash
# 백업
cp ~/.cursor/mcp.json ~/.cursor/mcp.json.backup

# 새 설정 파일 작성 (API 키는 본인의 것으로 교체)
cat > ~/.cursor/mcp.json << 'EOF'
{
  "mcpServers": {
    "TestSprite": {
      "command": "npx",
      "args": [
        "-y",
        "@testsprite/testsprite-mcp@latest"
      ],
      "env": {
        "API_KEY": "YOUR_API_KEY_HERE"
      }
    }
  }
}
EOF

# Cursor IDE 재시작
```

### 방법 4: 전역 설치로 변경

```bash
# 전역 설치
npm install -g @testsprite/testsprite-mcp

# 설정 파일 수정
cat > ~/.cursor/mcp.json << 'EOF'
{
  "mcpServers": {
    "TestSprite": {
      "command": "testsprite-mcp",
      "env": {
        "API_KEY": "YOUR_API_KEY_HERE"
      }
    }
  }
}
EOF

# Cursor IDE 재시작
```

### 방법 5: Cursor IDE 개발자 도구에서 확인

1. **Cursor IDE 열기**
2. **`Cmd+Option+I` (또는 `Help → Toggle Developer Tools`)**
3. **Console 탭 확인**
4. **다음 명령어 입력**:
```javascript
// MCP 서버 상태 확인
console.log(window.mcpServers);

// 또는
// MCP 관련 에러 확인
```

5. **에러 메시지 확인 및 해결**

---

## 🔍 진단 명령어

### MCP 서버 상태 확인

```bash
# 프로세스 확인
ps aux | grep testsprite

# 포트 사용 확인
lsof -i -P | grep testsprite

# 로그 확인 (가능한 경우)
tail -f ~/.cursor/*.log 2>/dev/null
```

### API 키 유효성 확인

```bash
# API 키로 TestSprite API 테스트
curl -H "Authorization: Bearer YOUR_API_KEY" \
  https://api.testsprite.com/v1/health 2>&1 | head -10
```

---

## 🎯 단계별 해결 체크리스트

### Step 1: 기본 확인
- [ ] Node.js v22 이상 설치됨
- [ ] npm/npx 정상 작동
- [ ] 네트워크 연결 정상
- [ ] API 키 유효함

### Step 2: MCP 서버 확인
- [ ] MCP 서버 프로세스 실행 중
- [ ] MCP 설정 파일 형식 정상
- [ ] API 키가 설정 파일에 올바르게 입력됨

### Step 3: Cursor IDE 확인
- [ ] Cursor IDE 최신 버전
- [ ] MCP 기능 지원 버전
- [ ] MCP 패널에서 서버 상태 확인
- [ ] 개발자 도구에서 에러 없음

### Step 4: 재시작 시도
- [ ] MCP 서버 프로세스 종료
- [ ] Cursor IDE 완전 종료
- [ ] 5초 대기
- [ ] Cursor IDE 재시작
- [ ] 프로젝트 폴더 다시 열기

---

## 💡 특별한 경우

### 경우 1: Cursor IDE 버전이 오래된 경우

```bash
# Cursor IDE 업데이트 확인
# Help → Check for Updates

# 또는 수동 다운로드
# https://cursor.sh/download
```

### 경우 2: macOS 권한 문제

```bash
# 시스템 설정 → 개인 정보 보호 및 보안
# 터미널 또는 Cursor에 전체 디스크 접근 권한 부여
```

### 경우 3: npm/npx 캐시 문제

```bash
# 캐시 정리
npm cache clean --force
rm -rf ~/.npm/_npx

# TestSprite MCP 재설치
npx @testsprite/testsprite-mcp@latest --force
```

### 경우 4: 여러 Cursor 인스턴스 실행 중

```bash
# 모든 Cursor 프로세스 확인
ps aux | grep -i cursor

# 모두 종료
killall Cursor
killall "Cursor Helper"

# 하나만 실행
```

---

## 🆘 여전히 해결되지 않는 경우

1. **TestSprite 공식 문서 확인**
   - https://docs.testsprite.com/mcp/troubleshooting

2. **Cursor IDE 커뮤니티 확인**
   - Cursor Discord 또는 포럼

3. **TestSprite 지원팀 문의**
   - 문제 재현 단계
   - 에러 로그
   - 시스템 정보

---

## 📝 참고 정보

**현재 확인된 상태**:
- MCP 서버 프로세스: ✅ 실행 중
- MCP 설정 파일: ✅ 존재
- API 키: ✅ 설정됨
- Node.js 버전: ✅ v22.16.0
- Cursor IDE 인식: ❌ 실패

**가장 가능성 높은 원인**:
1. Cursor IDE가 MCP 서버와의 통신 실패
2. MCP 프로토콜 버전 불일치
3. Cursor IDE 버전 문제
4. 권한 문제

**권장 해결 순서**:
1. Cursor IDE 완전 재시작 (방법 1)
2. MCP 설정 파일 재검증 (방법 3)
3. 전역 설치로 변경 (방법 4)
4. 개발자 도구에서 에러 확인 (방법 5)

---

**마지막 업데이트**: 2025-01-17
