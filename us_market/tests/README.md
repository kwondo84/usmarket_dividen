# Backend 테스트 스위트

이 디렉토리는 `us_market` 백엔드 코드에 대한 포괄적인 테스트를 포함합니다.

## 테스트 구조

### 테스트 파일

1. **test_engine.py** - DividendEngine 테스트
   - 포트폴리오 생성 기능
   - 테마 및 티어 조회
   - 필터링 및 제약 조건 검증
   - 자본 요구사항 계산
   - 월별 현금흐름 차트 데이터

2. **test_dividend_analyzer.py** - DividendAnalyzer 테스트
   - 배당 지속가능성 분석
   - Payout Ratio 계산
   - 배당 성장률 계산
   - 배당 연속 지급 연수
   - 안전성 점수 계산

3. **test_portfolio_optimizer.py** - PortfolioOptimizer 테스트
   - Risk Parity 최적화
   - Max Sharpe 최적화
   - 통합 최적화 인터페이스
   - 제약 조건 처리

4. **test_risk_analytics.py** - RiskAnalytics 테스트
   - 변동성 계산
   - 최대 낙폭 계산
   - Sharpe Ratio 계산
   - 통합 리스크 메트릭

5. **test_backtest.py** - BacktestEngine 테스트
   - 백테스트 실행
   - 수익률 계산
   - 리스크 메트릭 계산
   - 벤치마크 비교

6. **test_flask_api.py** - Flask API 엔드포인트 테스트
   - API 라우트 테스트
   - 요청/응답 검증
   - 에러 핸들링 테스트

## 테스트 실행

### pytest 설치

```bash
pip install pytest pytest-cov pytest-mock
```

### 테스트 실행

```bash
# 모든 테스트 실행
pytest us_market/tests/ -v

# 특정 테스트 파일 실행
pytest us_market/tests/test_engine.py -v

# 커버리지 포함 실행
pytest us_market/tests/ --cov=us_market --cov-report=html
```

## 테스트 커버리지

현재 테스트는 다음 기능을 커버합니다:

- ✅ DividendEngine의 모든 주요 메서드
- ✅ DividendAnalyzer의 모든 분석 기능
- ✅ PortfolioOptimizer의 최적화 알고리즘
- ✅ RiskAnalytics의 리스크 계산
- ✅ BacktestEngine의 백테스트 기능
- ✅ Flask API의 모든 엔드포인트

## 주의사항

일부 테스트는 외부 API(yfinance)에 의존하므로, 실제 네트워크 요청이 필요할 수 있습니다. 
테스트에서는 가능한 한 mock을 사용하여 외부 의존성을 최소화했습니다.
