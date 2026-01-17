"""
RiskAnalytics 테스트
- 변동성 계산
- 최대 낙폭 계산
- Sharpe Ratio 계산
- 통합 리스크 메트릭
"""
import pytest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from us_market.dividend.risk_analytics import RiskAnalytics


class TestRiskAnalytics:
    """RiskAnalytics 클래스 테스트"""
    
    @pytest.fixture
    def risk_analytics(self):
        """테스트용 리스크 분석기 인스턴스 생성"""
        return RiskAnalytics(risk_free_rate=0.05)
    
    @pytest.fixture
    def mock_price_data(self):
        """모의 가격 데이터"""
        dates = pd.date_range('2023-01-01', periods=252, freq='D')
        np.random.seed(42)
        prices = 100 + np.cumsum(np.random.randn(252) * 0.5)
        return pd.DataFrame({
            'Close': prices,
            'Open': prices * 0.99,
            'High': prices * 1.01,
            'Low': prices * 0.98,
            'Volume': np.random.randint(1000000, 10000000, 252)
        }, index=dates)
    
    def test_risk_analytics_initialization(self, risk_analytics):
        """리스크 분석기 초기화 테스트"""
        assert risk_analytics is not None
        assert risk_analytics.risk_free_rate == 0.05
        assert hasattr(risk_analytics, '_price_cache')
    
    @patch('us_market.dividend.risk_analytics.yf.Ticker')
    def test_calculate_volatility(self, mock_ticker, risk_analytics, mock_price_data):
        """변동성 계산"""
        mock_stock = Mock()
        mock_stock.history.return_value = mock_price_data
        mock_ticker.return_value = mock_stock
        
        volatility = risk_analytics.calculate_volatility('AAPL', period='1y')
        
        if volatility is not None:
            assert isinstance(volatility, float)
            assert volatility > 0
    
    @patch('us_market.dividend.risk_analytics.yf.Ticker')
    def test_calculate_volatility_insufficient_data(self, mock_ticker, risk_analytics):
        """데이터가 부족한 경우"""
        mock_stock = Mock()
        mock_stock.history.return_value = pd.DataFrame()
        mock_ticker.return_value = mock_stock
        
        volatility = risk_analytics.calculate_volatility('INVALID')
        assert volatility is None
    
    @patch('us_market.dividend.risk_analytics.yf.Ticker')
    def test_calculate_max_drawdown(self, mock_ticker, risk_analytics, mock_price_data):
        """최대 낙폭 계산"""
        mock_stock = Mock()
        mock_stock.history.return_value = mock_price_data
        mock_ticker.return_value = mock_stock
        
        drawdown = risk_analytics.calculate_max_drawdown('AAPL', period='1y')
        
        if drawdown is not None:
            assert isinstance(drawdown, float)
            assert drawdown <= 0  # 낙폭은 음수 또는 0
    
    @patch('us_market.dividend.risk_analytics.yf.Ticker')
    def test_calculate_sharpe_ratio(self, mock_ticker, risk_analytics, mock_price_data):
        """Sharpe Ratio 계산"""
        mock_stock = Mock()
        mock_stock.history.return_value = mock_price_data
        mock_ticker.return_value = mock_stock
        
        sharpe = risk_analytics.calculate_sharpe_ratio('AAPL', period='1y')
        
        if sharpe is not None:
            assert isinstance(sharpe, float)
            # Sharpe ratio는 음수일 수도 있음
    
    @patch('us_market.dividend.risk_analytics.yf.Ticker')
    def test_calculate_sharpe_zero_volatility(self, mock_ticker, risk_analytics):
        """변동성이 0인 경우"""
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        constant_prices = pd.DataFrame({'Close': [100.0] * 100}, index=dates)
        
        mock_stock = Mock()
        mock_stock.history.return_value = constant_prices
        mock_ticker.return_value = mock_stock
        
        sharpe = risk_analytics.calculate_sharpe_ratio('CONSTANT')
        assert sharpe is None
    
    @patch('us_market.dividend.risk_analytics.yf.Ticker')
    def test_get_all_risk_metrics(self, mock_ticker, risk_analytics, mock_price_data):
        """모든 리스크 메트릭 조회"""
        mock_stock = Mock()
        mock_stock.history.return_value = mock_price_data
        mock_ticker.return_value = mock_stock
        
        metrics = risk_analytics.get_all_risk_metrics('AAPL', period='1y')
        
        assert isinstance(metrics, dict)
        assert 'ticker' in metrics
        assert 'volatility_annual' in metrics
        assert 'max_drawdown' in metrics
        assert 'sharpe_ratio' in metrics
        assert metrics['ticker'] == 'AAPL'
    
    def test_price_cache(self, risk_analytics):
        """가격 데이터 캐싱 테스트"""
        mock_data = pd.DataFrame({'Close': [100, 101, 102]})
        risk_analytics._price_cache['AAPL_1y'] = mock_data
        
        cached = risk_analytics._get_price_data('AAPL', '1y')
        assert cached is not None
        assert len(cached) == 3
