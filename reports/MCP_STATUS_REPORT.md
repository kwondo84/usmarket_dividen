# TestSprite MCP 서버 연결 상태 보고서

## 📋 확인 결과 요약

### ✅ 설정 확인 완료

1. **MCP 설정 파일 위치**: `~/.cursor/mcp.json`
2. **TestSprite MCP 서버 설정**: ✅ 구성됨
3. **Node.js 버전**: v22.16.0 ✅ (요구사항: v22 이상)
4. **API 키**: ✅ 설정됨 (부분 마스킹: `sk-user-ubIIbJV-HxeW...KVJHKA2TahF57nTsroO8`)

### ⚠️ 현재 상태

**MCP 리소스 연결 상태**: ❌ 연결되지 않음

`list_mcp_resources` 도구를 통해 확인한 결과, 현재 TestSprite MCP 서버에서 제공하는 리소스가 감지되지 않았습니다.

## 📝 MCP 설정 상세

### 설정 파일 내용 (`~/.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "TestSprite": {
      "command": "npx @testsprite/testsprite-mcp@latest",
      "env": {
        "API_KEY": "sk-user-ubIIbJV-HxeW...KVJHKA2TahF57nTsroO8"
      },
      "args": []
    }
  }
}
```

### 설정 분석

- ✅ **서버 이름**: `TestSprite`
- ✅ **실행 명령어**: `npx @testsprite/testsprite-mcp@latest`
- ✅ **API 키**: 환경 변수로 설정됨
- ✅ **인자**: 없음 (기본 설정)

## 🔍 문제 진단

### 가능한 원인

1. **MCP 서버가 실행되지 않음**
   - Cursor IDE가 MCP 서버를 시작하지 않았을 수 있음
   - 서버 시작에 시간이 걸릴 수 있음

2. **API 키 문제**
   - API 키가 만료되었거나 유효하지 않을 수 있음
   - API 키 권한이 부족할 수 있음

3. **네트워크 연결 문제**
   - TestSprite 서버에 연결할 수 없을 수 있음
   - 방화벽이나 프록시 설정 문제

4. **MCP 서버 설치 문제**
   - `npx @testsprite/testsprite-mcp@latest` 실행 시 권한 문제 발생
   - npm/npx 권한 설정 필요

## 🛠️ 해결 방법

### 1. Cursor IDE 재시작
```bash
# Cursor IDE를 완전히 종료한 후 다시 시작
# MCP 서버가 자동으로 시작되어야 함
```

### 2. MCP 서버 상태 확인
- Cursor IDE의 MCP 패널에서 TestSprite 서버 상태 확인
- 초록색(연결됨) / 빨간색(연결 안됨) / 노란색(연결 중) 상태 확인

### 3. API 키 재확인
- TestSprite 대시보드에서 API 키 확인
- Settings → API Keys에서 키 상태 확인
- 필요시 새 API 키 생성

### 4. 수동으로 MCP 서버 테스트
```bash
# TestSprite MCP 서버가 정상 작동하는지 확인
npx @testsprite/testsprite-mcp@latest --version

# 또는 도움말 확인
npx @testsprite/testsprite-mcp@latest --help
```

### 5. 로그 확인
- Cursor IDE의 개발자 도구에서 MCP 관련 에러 로그 확인
- `Help → Toggle Developer Tools → Console`에서 에러 메시지 확인

## 📊 권장 사항

### 즉시 시도할 수 있는 방법

1. **Cursor IDE 재시작** (가장 간단한 해결책)
2. **MCP 서버 토글 OFF → ON** (Cursor 설정에서)
3. **API 키 재확인** (TestSprite 대시보드)

### 추가 확인 사항

1. **Node.js 버전**: ✅ v22.16.0 (요구사항 충족)
2. **npm/npx 권한**: ⚠️ 권한 문제 가능성 (EPERM 에러 발생)
3. **네트워크 연결**: 확인 필요

## 🎯 TestSprite 사용 방법

MCP 서버가 연결되면 다음 명령어로 테스트를 실행할 수 있습니다:

```
Hey, test this project with TestSprite (테스트폴더는 @us_market 기준으로, 백엔드 코드 구조/API를 중심으로)
```

또는 직접 MCP 리소스를 사용하여:
- 프로젝트 분석
- 테스트 계획 생성
- 테스트 실행
- 결과 보고서 생성

## 📞 추가 지원

문제가 지속되면:
1. TestSprite 공식 문서: https://docs.testsprite.com
2. MCP 트러블슈팅 가이드: https://docs.testsprite.com/mcp/troubleshooting
3. Cursor IDE MCP 설정 확인

---

**보고서 생성 시간**: 2025-01-17
**확인된 설정**: MCP 설정 파일, Node.js 버전, API 키 존재
**현재 상태**: MCP 리소스 연결 안됨 (서버 실행 상태 확인 필요)
