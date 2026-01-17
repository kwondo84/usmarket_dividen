"""
Flask API 엔드포인트 테스트
- API 라우트 테스트
- 요청/응답 검증
- 에러 핸들링 테스트
"""
import pytest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from flask import Flask
from flask_app import app


class TestFlaskAPI:
    """Flask API 엔드포인트 테스트"""
    
    @pytest.fixture
    def client(self):
        """테스트용 Flask 클라이언트"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_index_route(self, client):
        """인덱스 페이지 라우트 테스트"""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_dashboard_route(self, client):
        """대시보드 페이지 라우트 테스트"""
        response = client.get('/app')
        assert response.status_code == 200
    
    def test_dividend_page_route(self, client):
        """배당 페이지 라우트 테스트"""
        response = client.get('/dividend')
        assert response.status_code == 200
    
    def test_get_dividend_themes(self, client):
        """배당 테마 목록 조회 API 테스트"""
        with patch('us_market.dividend.engine.DividendEngine') as mock_engine_class:
            mock_engine = Mock()
            mock_engine.get_themes.return_value = [
                {'id': 'test_theme', 'title': 'Test Theme', 'subtitle': 'Test'}
            ]
            mock_engine_class.return_value = mock_engine
            
            response = client.get('/api/dividend/themes')
            assert response.status_code == 200
            data = json.loads(response.data)
            assert isinstance(data, list)
    
    def test_get_dividend_themes_error(self, client):
        """배당 테마 목록 조회 에러 핸들링"""
        with patch('us_market.dividend.engine.DividendEngine') as mock_engine_class:
            mock_engine_class.side_effect = Exception('Test error')
            
            response = client.get('/api/dividend/themes')
            assert response.status_code == 500
            data = json.loads(response.data)
            assert 'error' in data
    
    def test_get_all_tier_portfolios(self, client):
        """모든 티어 포트폴리오 생성 API 테스트"""
        with patch('us_market.dividend.engine.DividendEngine') as mock_engine_class:
            mock_engine = Mock()
            mock_engine.generate_portfolio.return_value = {
                'theme_id': 'test',
                'tier_id': 'balanced',
                'required_capital_krw': 10000000,
                'allocation': []
            }
            mock_engine_class.return_value = mock_engine
            
            response = client.post(
                '/api/dividend/all-tiers',
                json={
                    'theme_id': 'max_monthly_income',
                    'target_monthly_krw': 1000000,
                    'fx_rate': 1420,
                    'tax_rate': 15.4,
                    'optimize_mode': 'greedy'
                },
                content_type='application/json'
            )
            assert response.status_code == 200
            data = json.loads(response.data)
            assert isinstance(data, dict)
            assert 'defensive' in data
            assert 'balanced' in data
            assert 'aggressive' in data
    
    def test_get_all_tier_portfolios_default_params(self, client):
        """기본 파라미터로 포트폴리오 생성"""
        with patch('us_market.dividend.engine.DividendEngine') as mock_engine_class:
            mock_engine = Mock()
            mock_engine.generate_portfolio.return_value = {
                'theme_id': 'max_monthly_income',
                'tier_id': 'balanced',
                'required_capital_krw': 10000000,
                'allocation': []
            }
            mock_engine_class.return_value = mock_engine
            
            response = client.post(
                '/api/dividend/all-tiers',
                json={},
                content_type='application/json'
            )
            assert response.status_code == 200
    
    def test_get_dividend_risk_metrics(self, client):
        """배당 리스크 메트릭 조회 API 테스트"""
        with patch('us_market.dividend.risk_analytics.RiskAnalytics') as mock_risk_class:
            mock_risk = Mock()
            mock_risk.get_all_risk_metrics.return_value = {
                'ticker': 'AAPL',
                'volatility_annual': 0.20,
                'max_drawdown': -0.15,
                'sharpe_ratio': 1.5,
                'risk_grade': 'B'
            }
            mock_risk_class.return_value = mock_risk
            
            response = client.get('/api/dividend/risk-metrics/AAPL')
            assert response.status_code == 200
            data = json.loads(response.data)
            assert 'ticker' in data
            assert 'risk_grade' in data
    
    def test_get_dividend_risk_metrics_with_period(self, client):
        """기간 파라미터 포함 리스크 메트릭 조회"""
        with patch('us_market.dividend.risk_analytics.RiskAnalytics') as mock_risk_class:
            mock_risk = Mock()
            mock_risk.get_all_risk_metrics.return_value = {
                'ticker': 'AAPL',
                'volatility_annual': 0.20,
                'max_drawdown': -0.15,
                'sharpe_ratio': 1.5
            }
            mock_risk_class.return_value = mock_risk
            
            response = client.get('/api/dividend/risk-metrics/AAPL?period=2y')
            assert response.status_code == 200
    
    def test_get_dividend_sustainability(self, client):
        """배당 지속가능성 분석 API 테스트"""
        with patch('us_market.dividend.dividend_analyzer.DividendAnalyzer') as mock_analyzer_class:
            mock_analyzer = Mock()
            mock_analyzer.get_all_metrics.return_value = {
                'payout_ratio': 0.5,
                'dividend_growth_5y': 0.05,
                'dividend_streak': 10,
                'safety': {
                    'safety_score': 75,
                    'safety_grade': 'B'
                }
            }
            mock_analyzer_class.return_value = mock_analyzer
            
            response = client.get('/api/dividend/sustainability/AAPL')
            assert response.status_code == 200
            data = json.loads(response.data)
            assert 'payout_ratio' in data
            assert 'safety' in data
    
    def test_optimize_dividend_advanced(self, client):
        """고급 포트폴리오 최적화 API 테스트"""
        with patch('us_market.dividend.engine.DividendEngine') as mock_engine_class:
            mock_engine = Mock()
            mock_engine.generate_portfolio.return_value = {
                'theme_id': 'max_monthly_income',
                'tier_id': 'balanced',
                'required_capital_krw': 10000000,
                'allocation': [],
                'optimize_mode': 'risk_parity'
            }
            mock_engine_class.return_value = mock_engine
            
            response = client.post(
                '/api/dividend/optimize-advanced',
                json={
                    'theme_id': 'max_monthly_income',
                    'tier_id': 'balanced',
                    'target_monthly_krw': 1000000,
                    'optimize_mode': 'risk_parity'
                },
                content_type='application/json'
            )
            assert response.status_code == 200
            data = json.loads(response.data)
            assert 'optimize_mode' in data
    
    def test_run_dividend_backtest(self, client):
        """배당 포트폴리오 백테스트 API 테스트"""
        with patch('us_market.dividend.backtest.BacktestEngine') as mock_backtest_class:
            mock_backtest = Mock()
            mock_backtest.run_backtest.return_value = {
                'start_date': '2022-01-01',
                'end_date': '2022-12-31',
                'initial_capital': 100000,
                'final_value': 110000,
                'total_return': 0.10,
                'cagr': 0.10,
                'max_drawdown': -0.05,
                'sharpe_ratio': 1.5
            }
            mock_backtest_class.return_value = mock_backtest
            
            response = client.post(
                '/api/dividend/backtest',
                json={
                    'portfolio': [
                        {'ticker': 'AAPL', 'weight': 0.5},
                        {'ticker': 'MSFT', 'weight': 0.5}
                    ],
                    'start_date': '2022-01-01',
                    'end_date': '2022-12-31',
                    'initial_capital': 100000
                },
                content_type='application/json'
            )
            assert response.status_code == 200
            data = json.loads(response.data)
            assert 'total_return' in data
            assert 'cagr' in data
    
    def test_run_dividend_backtest_no_portfolio(self, client):
        """포트폴리오가 없는 경우 에러 처리"""
        response = client.post(
            '/api/dividend/backtest',
            json={},
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
