# TestSprite MCP 설정 UI 문제 해결 가이드

## 🔍 현재 상황

**문제**: TestSprite MCP 서버가 연결되어도 설정 UI가 나타나지 않음

**확인된 사항**:
- ✅ MCP 서버 프로세스 실행 중 (`testsprite-mcp-plugin`)
- ✅ MCP 설정 파일 존재 (`~/.cursor/mcp.json`)
- ✅ API 키 설정됨
- ✅ Node.js v22.16.0 (요구사항 충족)
- ❌ MCP 리소스가 `list_mcp_resources`에서 감지되지 않음
- ❌ 설정 UI가 나타나지 않음

---

## 🎯 예상되는 정상 동작

TestSprite MCP가 제대로 연결되면 다음 UI가 나타나야 합니다:

### 1. 테스트 설정 화면 (이미지와 동일)
- **Testing Types**
  - Mode: Backend / Frontend 선택
  - Scope: Codebase / Code diff 선택
- **Authentication**
  - Type: None / API Key / OAuth 등
- **Local Development Port**
  - Port: `http://localhost:5001`
  - Path: `/`

### 2. 추가 UI 요소
- 프로젝트 구조 드래그/업로드 기능
- 진행 상태 표시
- 결과 리포트 화면

---

## 🔧 추가 진단 방법

### 1. Cursor IDE MCP 패널 확인

1. Cursor IDE 열기
2. MCP 패널 확인 (보통 사이드바 또는 하단 패널)
3. TestSprite 서버 상태 확인:
   - 🟢 초록색: 연결됨
   - 🔴 빨간색: 연결 안됨
   - 🟡 노란색: 연결 중

### 2. 개발자 도구에서 로그 확인

1. `Help → Toggle Developer Tools` (또는 `Cmd+Option+I`)
2. Console 탭에서 MCP 관련 에러 확인
3. Network 탭에서 MCP 통신 확인

### 3. MCP 서버 로그 확인

```bash
# MCP 서버 프로세스 확인
ps aux | grep testsprite

# 프로세스 ID 확인 후 로그 확인
# (Cursor IDE가 로그를 어디에 저장하는지 확인 필요)
```

### 4. TestSprite MCP 서버 수동 테스트

```bash
# MCP 서버가 직접 실행 가능한지 확인
npx @testsprite/testsprite-mcp@latest --help

# API 키로 인증 테스트
export API_KEY="sk-user-ubIIbJV-HxeW...KVJHKA2TahF57nTsroO8"
npx @testsprite/testsprite-mcp@latest
```

---

## 🛠️ 고급 해결 방법

### 방법 1: MCP 설정 파일 수정

현재 설정:
```json
{
  "mcpServers": {
    "TestSprite": {
      "command": "npx @testsprite/testsprite-mcp@latest",
      "env": {
        "API_KEY": "sk-user-..."
      },
      "args": []
    }
  }
}
```

**시도해볼 수정사항**:

1. **전역 설치 사용**:
```json
{
  "mcpServers": {
    "TestSprite": {
      "command": "testsprite-mcp",
      "env": {
        "API_KEY": "sk-user-..."
      },
      "args": []
    }
  }
}
```
그리고 전역 설치:
```bash
npm install -g @testsprite/testsprite-mcp
```

2. **명시적 경로 지정**:
```json
{
  "mcpServers": {
    "TestSprite": {
      "command": "node",
      "args": [
        "/usr/local/bin/npx",
        "@testsprite/testsprite-mcp@latest"
      ],
      "env": {
        "API_KEY": "sk-user-..."
      }
    }
  }
}
```

### 방법 2: Cursor IDE 버전 확인

TestSprite MCP는 최신 버전의 Cursor IDE가 필요할 수 있습니다:

1. `Help → About`에서 버전 확인
2. 최신 버전으로 업데이트
3. MCP 기능이 지원되는 버전인지 확인

### 방법 3: MCP 프로토콜 버전 확인

TestSprite MCP 서버가 지원하는 MCP 프로토콜 버전과 Cursor IDE가 지원하는 버전이 일치하는지 확인:

1. TestSprite MCP 문서에서 요구사항 확인
2. Cursor IDE 문서에서 MCP 지원 버전 확인

### 방법 4: API 키 재생성

1. TestSprite 대시보드 접속
2. Settings → API Keys
3. 기존 키 삭제 또는 비활성화
4. 새 API 키 생성
5. `~/.cursor/mcp.json`에 새 키 입력
6. Cursor IDE 재시작

### 방법 5: MCP 서버 재설치

```bash
# 캐시 정리
npm cache clean --force

# npx 캐시 정리
rm -rf ~/.npm/_npx

# TestSprite MCP 재설치
npm install -g @testsprite/testsprite-mcp

# 또는 최신 버전 강제 설치
npx @testsprite/testsprite-mcp@latest --force
```

### 방법 6: Cursor IDE 설정 초기화

⚠️ 주의: 이 방법은 다른 설정도 초기화될 수 있습니다.

1. Cursor IDE 완전 종료
2. 설정 파일 백업:
```bash
cp ~/.cursor/mcp.json ~/.cursor/mcp.json.backup
```
3. Cursor IDE 재시작
4. MCP 설정 다시 추가

---

## 🔍 추가 확인 사항

### 1. 네트워크 연결

TestSprite MCP 서버가 TestSprite API 서버에 연결할 수 있는지 확인:

```bash
# TestSprite API 서버 연결 테스트
curl -I https://api.testsprite.com 2>&1 | head -5

# 또는
ping api.testsprite.com
```

### 2. 방화벽/프록시 설정

회사 네트워크나 방화벽이 MCP 통신을 차단할 수 있습니다:

1. 방화벽 설정 확인
2. 프록시 설정 확인
3. VPN 연결 상태 확인

### 3. 권한 문제

npm/npx 권한 문제가 있을 수 있습니다:

```bash
# npm 전역 설치 권한 확인
npm config get prefix

# 필요시 권한 수정
sudo chown -R $(whoami) $(npm config get prefix)/{lib/node_modules,bin,share}
```

---

## 📞 TestSprite 지원팀 문의

위 방법들을 모두 시도해도 해결되지 않으면:

1. **TestSprite 공식 문서**: https://docs.testsprite.com
2. **MCP 트러블슈팅 가이드**: https://docs.testsprite.com/mcp/troubleshooting
3. **GitHub Issues**: TestSprite MCP 관련 이슈 확인
4. **TestSprite 지원팀**: 직접 문의

**문의 시 포함할 정보**:
- Cursor IDE 버전
- Node.js 버전
- TestSprite MCP 버전
- MCP 설정 파일 (API 키 제외)
- 에러 로그
- 문제 재현 단계

---

## 🎯 빠른 체크리스트

- [ ] Cursor IDE 최신 버전인가?
- [ ] Node.js v22 이상인가?
- [ ] MCP 서버 프로세스가 실행 중인가?
- [ ] API 키가 유효한가?
- [ ] 네트워크 연결이 정상인가?
- [ ] 방화벽/프록시가 차단하지 않는가?
- [ ] npm/npx 권한이 정상인가?
- [ ] Cursor IDE MCP 패널에서 상태 확인
- [ ] 개발자 도구에서 에러 로그 확인
- [ ] TestSprite 대시보드에서 API 키 상태 확인

---

**마지막 업데이트**: 2025-01-17  
**문제 상태**: MCP 서버 실행 중이지만 UI 미표시
