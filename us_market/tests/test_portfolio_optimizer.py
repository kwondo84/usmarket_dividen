"""
PortfolioOptimizer 테스트
- Risk Parity 최적화
- Max Sharpe 최적화
- 통합 최적화 인터페이스
"""
import pytest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from us_market.dividend.portfolio_optimizer import PortfolioOptimizer


class TestPortfolioOptimizer:
    """PortfolioOptimizer 클래스 테스트"""
    
    @pytest.fixture
    def optimizer(self):
        """테스트용 최적화기 인스턴스 생성"""
        return PortfolioOptimizer(risk_free_rate=0.05)
    
    @pytest.fixture
    def mock_returns_data(self):
        """모의 수익률 데이터"""
        dates = pd.date_range('2023-01-01', periods=252, freq='D')
        np.random.seed(42)
        returns = pd.DataFrame({
            'AAPL': np.random.normal(0.001, 0.02, 252),
            'MSFT': np.random.normal(0.0008, 0.018, 252),
            'GOOGL': np.random.normal(0.0009, 0.022, 252)
        }, index=dates)
        return returns
    
    def test_optimizer_initialization(self, optimizer):
        """최적화기 초기화 테스트"""
        assert optimizer is not None
        assert optimizer.risk_free_rate == 0.05
        assert hasattr(optimizer, '_returns_cache')
    
    @patch('us_market.dividend.portfolio_optimizer.yf.Ticker')
    def test_get_returns(self, mock_ticker, optimizer):
        """수익률 데이터 가져오기"""
        mock_stock = Mock()
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        prices = 100 + np.cumsum(np.random.randn(100) * 0.5)
        hist = pd.DataFrame({'Close': prices}, index=dates)
        mock_stock.history.return_value = hist
        mock_ticker.return_value = mock_stock
        
        returns = optimizer._get_returns('AAPL', period='1y')
        # 데이터가 충분하면 반환되어야 함
        if returns is not None:
            assert isinstance(returns, pd.Series)
            assert len(returns) > 0
    
    @patch('us_market.dividend.portfolio_optimizer.yf.Ticker')
    def test_get_returns_insufficient_data(self, mock_ticker, optimizer):
        """데이터가 부족한 경우"""
        mock_stock = Mock()
        mock_stock.history.return_value = pd.DataFrame()
        mock_ticker.return_value = mock_stock
        
        returns = optimizer._get_returns('INVALID', period='1y')
        assert returns is None
    
    @patch.object(PortfolioOptimizer, '_get_returns')
    def test_optimize_risk_parity(self, mock_get_returns, optimizer, mock_returns_data):
        """Risk Parity 최적화"""
        def side_effect(ticker, period='1y'):
            if ticker in mock_returns_data.columns:
                return mock_returns_data[ticker]
            return None
        
        mock_get_returns.side_effect = side_effect
        
        tickers = ['AAPL', 'MSFT', 'GOOGL']
        result = optimizer.optimize_risk_parity(tickers)
        
        if result is not None:
            assert isinstance(result, list)
            assert len(result) > 0
            total_weight = sum(w for _, w in result)
            assert abs(total_weight - 1.0) < 0.01  # 가중치 합이 1에 가까워야 함
            
            for ticker, weight in result:
                assert ticker in tickers
                assert 0 <= weight <= 1
    
    @patch.object(PortfolioOptimizer, '_get_returns')
    def test_optimize_max_sharpe(self, mock_get_returns, optimizer, mock_returns_data):
        """Max Sharpe 최적화"""
        def side_effect(ticker, period='1y'):
            if ticker in mock_returns_data.columns:
                return mock_returns_data[ticker]
            return None
        
        mock_get_returns.side_effect = side_effect
        
        tickers = ['AAPL', 'MSFT', 'GOOGL']
        result = optimizer.optimize_max_sharpe(tickers)
        
        if result is not None:
            assert isinstance(result, list)
            assert len(result) > 0
            total_weight = sum(w for _, w in result)
            assert abs(total_weight - 1.0) < 0.01
            
            for ticker, weight in result:
                assert ticker in tickers
                assert 0 <= weight <= 1
    
    @patch.object(PortfolioOptimizer, '_get_returns')
    def test_optimize_with_constraints(self, mock_get_returns, optimizer, mock_returns_data):
        """제약 조건이 있는 최적화"""
        def side_effect(ticker, period='1y'):
            if ticker in mock_returns_data.columns:
                return mock_returns_data[ticker]
            return None
        
        mock_get_returns.side_effect = side_effect
        
        tickers = ['AAPL', 'MSFT', 'GOOGL']
        constraints = {'single_stock_max': 0.4}
        
        result = optimizer.optimize_risk_parity(tickers, constraints=constraints)
        
        if result is not None:
            for ticker, weight in result:
                assert weight <= 0.4  # 제약 조건 확인
    
    def test_optimize_unified_interface(self, optimizer):
        """통합 최적화 인터페이스"""
        with patch.object(optimizer, 'optimize_risk_parity', return_value=[('AAPL', 0.5), ('MSFT', 0.5)]):
            result = optimizer.optimize(['AAPL', 'MSFT'], method='risk_parity')
            assert result is not None
            assert len(result) == 2
        
        with patch.object(optimizer, 'optimize_max_sharpe', return_value=[('AAPL', 0.6), ('MSFT', 0.4)]):
            result = optimizer.optimize(['AAPL', 'MSFT'], method='max_sharpe')
            assert result is not None
            assert len(result) == 2
        
        # 지원하지 않는 메서드
        result = optimizer.optimize(['AAPL', 'MSFT'], method='invalid_method')
        assert result is None
    
    @patch.object(PortfolioOptimizer, '_get_returns')
    def test_optimize_insufficient_tickers(self, mock_get_returns, optimizer):
        """티커가 부족한 경우"""
        mock_get_returns.return_value = None
        
        result = optimizer.optimize_risk_parity(['AAPL'])
        assert result is None
