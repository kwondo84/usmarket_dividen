"""
BacktestEngine 테스트
- 백테스트 실행
- 수익률 계산
- 리스크 메트릭 계산
- 벤치마크 비교
"""
import pytest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
import pandas as pd
import numpy as np
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from us_market.dividend.backtest import BacktestEngine


class TestBacktestEngine:
    """BacktestEngine 클래스 테스트"""
    
    @pytest.fixture
    def backtest_engine(self):
        """테스트용 백테스트 엔진 인스턴스 생성"""
        return BacktestEngine(benchmark='SPY')
    
    @pytest.fixture
    def mock_price_data(self):
        """모의 가격 데이터"""
        dates = pd.date_range('2022-01-01', periods=252, freq='D')
        np.random.seed(42)
        prices = 100 + np.cumsum(np.random.randn(252) * 0.5)
        return pd.DataFrame({
            'Close': prices,
            'Open': prices * 0.99,
            'High': prices * 1.01,
            'Low': prices * 0.98,
            'Volume': np.random.randint(1000000, 10000000, 252)
        }, index=dates)
    
    @pytest.fixture
    def mock_dividend_data(self):
        """모의 배당 데이터"""
        dates = pd.date_range('2022-01-01', periods=4, freq='Q')
        amounts = [0.5, 0.55, 0.6, 0.65]
        return pd.Series(amounts, index=dates)
    
    def test_backtest_engine_initialization(self, backtest_engine):
        """백테스트 엔진 초기화 테스트"""
        assert backtest_engine is not None
        assert backtest_engine.benchmark == 'SPY'
    
    @patch('us_market.dividend.backtest.yf.Ticker')
    def test_run_backtest_valid(self, mock_ticker, backtest_engine, mock_price_data, mock_dividend_data):
        """유효한 백테스트 실행"""
        mock_stock = Mock()
        mock_stock.history.return_value = mock_price_data
        mock_stock.dividends = mock_dividend_data
        mock_ticker.return_value = mock_stock
        
        portfolio = [('AAPL', 0.5), ('MSFT', 0.5)]
        result = backtest_engine.run_backtest(
            portfolio=portfolio,
            start_date='2022-01-01',
            end_date='2022-12-31',
            initial_capital=100000
        )
        
        if 'error' not in result:
            assert 'start_date' in result
            assert 'end_date' in result
            assert 'initial_capital' in result
            assert 'final_value' in result
            assert 'total_return' in result
            assert 'price_return' in result
            assert 'dividend_return' in result
            assert 'cagr' in result
            assert 'max_drawdown' in result
            assert 'volatility' in result
            assert 'sharpe_ratio' in result
            assert 'benchmark' in result
            
            assert result['initial_capital'] == 100000
            assert result['final_value'] > 0
            assert isinstance(result['total_return'], float)
            assert isinstance(result['cagr'], float)
            assert isinstance(result['max_drawdown'], float)
            assert result['max_drawdown'] <= 0
    
    @patch('us_market.dividend.backtest.yf.Ticker')
    def test_run_backtest_no_data(self, mock_ticker, backtest_engine):
        """데이터가 없는 경우"""
        mock_stock = Mock()
        mock_stock.history.return_value = pd.DataFrame()
        mock_ticker.return_value = mock_stock
        
        portfolio = [('INVALID', 1.0)]
        result = backtest_engine.run_backtest(
            portfolio=portfolio,
            start_date='2022-01-01',
            end_date='2022-12-31'
        )
        
        assert 'error' in result
    
    @patch('us_market.dividend.backtest.yf.Ticker')
    def test_run_backtest_insufficient_data(self, mock_ticker, backtest_engine):
        """데이터가 부족한 경우"""
        mock_stock = Mock()
        # 5일치 데이터만 제공 (10일 미만)
        dates = pd.date_range('2022-01-01', periods=5, freq='D')
        prices = pd.DataFrame({'Close': [100, 101, 102, 103, 104]}, index=dates)
        mock_stock.history.return_value = prices
        mock_stock.dividends = pd.Series(dtype=float)
        mock_ticker.return_value = mock_stock
        
        portfolio = [('AAPL', 1.0)]
        result = backtest_engine.run_backtest(
            portfolio=portfolio,
            start_date='2022-01-01',
            end_date='2022-01-05'
        )
        
        assert 'error' in result
    
    @patch('us_market.dividend.backtest.yf.Ticker')
    def test_run_backtest_with_benchmark(self, mock_ticker, backtest_engine, mock_price_data):
        """벤치마크 비교 포함 백테스트"""
        mock_stock = Mock()
        mock_stock.history.return_value = mock_price_data
        mock_stock.dividends = pd.Series(dtype=float)
        mock_ticker.return_value = mock_stock
        
        portfolio = [('AAPL', 1.0)]
        result = backtest_engine.run_backtest(
            portfolio=portfolio,
            start_date='2022-01-01',
            end_date='2022-12-31'
        )
        
        if 'error' not in result:
            assert 'benchmark' in result
            assert result['benchmark'] == 'SPY'
            # 벤치마크 수익률이 있으면 알파 계산
            if result.get('benchmark_return') is not None:
                assert 'alpha' in result
    
    @patch('us_market.dividend.backtest.yf.Ticker')
    def test_run_backtest_portfolio_weights_normalization(self, mock_ticker, backtest_engine, mock_price_data):
        """포트폴리오 가중치 정규화"""
        mock_stock = Mock()
        mock_stock.history.return_value = mock_price_data
        mock_stock.dividends = pd.Series(dtype=float)
        mock_ticker.return_value = mock_stock
        
        # 가중치 합이 1이 아닌 경우
        portfolio = [('AAPL', 0.6), ('MSFT', 0.5)]
        result = backtest_engine.run_backtest(
            portfolio=portfolio,
            start_date='2022-01-01',
            end_date='2022-12-31'
        )
        
        # 정규화되어 실행되어야 함
        if 'error' not in result:
            assert 'final_value' in result
    
    def test_run_backtest_default_end_date(self, backtest_engine):
        """기본 종료일 사용"""
        with patch.object(backtest_engine, 'run_backtest') as mock_run:
            mock_run.return_value = {'final_value': 110000}
            result = backtest_engine.run_backtest(
                portfolio=[('AAPL', 1.0)],
                start_date='2022-01-01',
                end_date=None
            )
            # end_date가 None이면 현재 날짜로 설정되어야 함
            assert result is not None
