"""
DividendAnalyzer 테스트
- 배당 지속가능성 분석
- Payout Ratio 계산
- 배당 성장률 계산
- 배당 연속 지급 연수
- 안전성 점수 계산
"""
import pytest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from us_market.dividend.dividend_analyzer import DividendAnalyzer


class TestDividendAnalyzer:
    """DividendAnalyzer 클래스 테스트"""
    
    @pytest.fixture
    def analyzer(self):
        """테스트용 분석기 인스턴스 생성"""
        return DividendAnalyzer()
    
    @pytest.fixture
    def mock_stock_info(self):
        """모의 주식 정보"""
        return {
            'dividendRate': 2.5,
            'trailingEps': 5.0,
            'currentPrice': 100.0
        }
    
    @pytest.fixture
    def mock_dividends(self):
        """모의 배당 데이터"""
        dates = pd.date_range('2020-01-01', periods=20, freq='Q')
        amounts = [0.5 + i * 0.05 for i in range(20)]
        return pd.Series(amounts, index=dates)
    
    def test_analyzer_initialization(self, analyzer):
        """분석기 초기화 테스트"""
        assert analyzer is not None
        assert hasattr(analyzer, '_info_cache')
    
    @patch('us_market.dividend.dividend_analyzer.yf.Ticker')
    def test_calculate_payout_ratio_valid(self, mock_ticker, analyzer, mock_stock_info):
        """유효한 데이터로 Payout Ratio 계산"""
        mock_stock = Mock()
        mock_stock.info = mock_stock_info
        mock_ticker.return_value = mock_stock
        
        ratio = analyzer.calculate_payout_ratio('AAPL')
        assert ratio is not None
        assert isinstance(ratio, float)
        # dividendRate / trailingEps = 2.5 / 5.0 = 0.5
        assert abs(ratio - 0.5) < 0.001
    
    @patch('us_market.dividend.dividend_analyzer.yf.Ticker')
    def test_calculate_payout_ratio_zero_eps(self, mock_ticker, analyzer):
        """EPS가 0인 경우"""
        mock_stock = Mock()
        mock_stock.info = {'dividendRate': 2.5, 'trailingEps': 0}
        mock_ticker.return_value = mock_stock
        
        ratio = analyzer.calculate_payout_ratio('AAPL')
        assert ratio is None
    
    @patch('us_market.dividend.dividend_analyzer.yf.Ticker')
    def test_calculate_payout_ratio_missing_data(self, mock_ticker, analyzer):
        """데이터가 없는 경우"""
        mock_stock = Mock()
        mock_stock.info = {}
        mock_ticker.return_value = mock_stock
        
        ratio = analyzer.calculate_payout_ratio('INVALID')
        assert ratio is None
    
    @patch('us_market.dividend.dividend_analyzer.yf.Ticker')
    def test_calculate_dividend_growth_rate(self, mock_ticker, analyzer, mock_dividends):
        """배당 성장률 계산"""
        mock_stock = Mock()
        mock_stock.dividends = mock_dividends
        mock_ticker.return_value = mock_stock
        
        growth = analyzer.calculate_dividend_growth_rate('AAPL', years=5)
        # 성장률이 계산되면 숫자여야 함
        if growth is not None:
            assert isinstance(growth, float)
    
    @patch('us_market.dividend.dividend_analyzer.yf.Ticker')
    def test_calculate_dividend_growth_rate_insufficient_data(self, mock_ticker, analyzer):
        """데이터가 부족한 경우"""
        mock_stock = Mock()
        mock_stock.dividends = pd.Series(dtype=float)
        mock_ticker.return_value = mock_stock
        
        growth = analyzer.calculate_dividend_growth_rate('AAPL')
        assert growth is None
    
    @patch('us_market.dividend.dividend_analyzer.yf.Ticker')
    def test_get_dividend_streak(self, mock_ticker, analyzer, mock_dividends):
        """배당 연속 지급 연수 계산"""
        mock_stock = Mock()
        mock_stock.dividends = mock_dividends
        mock_ticker.return_value = mock_stock
        
        streak = analyzer.get_dividend_streak('AAPL')
        assert isinstance(streak, int)
        assert streak >= 0
    
    @patch('us_market.dividend.dividend_analyzer.yf.Ticker')
    def test_get_dividend_streak_no_dividends(self, mock_ticker, analyzer):
        """배당이 없는 경우"""
        mock_stock = Mock()
        mock_stock.dividends = pd.Series(dtype=float)
        mock_ticker.return_value = mock_stock
        
        streak = analyzer.get_dividend_streak('AAPL')
        assert streak == 0
    
    @patch('us_market.dividend.dividend_analyzer.yf.Ticker')
    def test_get_dividend_safety_score(self, mock_ticker, analyzer, mock_stock_info, mock_dividends):
        """배당 안전성 점수 계산"""
        mock_stock = Mock()
        mock_stock.info = mock_stock_info
        mock_stock.dividends = mock_dividends
        mock_ticker.return_value = mock_stock
        
        score = analyzer.get_dividend_safety_score('AAPL')
        assert isinstance(score, dict)
        assert 'ticker' in score
        assert 'safety_score' in score
        assert 'safety_grade' in score
        assert 'breakdown' in score
        
        assert score['ticker'] == 'AAPL'
        assert isinstance(score['safety_score'], (int, float))
        assert 0 <= score['safety_score'] <= 100
        assert score['safety_grade'] in ['A', 'B', 'C', 'D']
        
        breakdown = score['breakdown']
        assert isinstance(breakdown, dict)
        if 'payout_ratio' in breakdown:
            assert 'value' in breakdown['payout_ratio']
            assert 'score' in breakdown['payout_ratio']
            assert 'max' in breakdown['payout_ratio']
    
    def test_get_all_metrics(self, analyzer):
        """모든 메트릭 조회"""
        with patch.object(analyzer, 'calculate_payout_ratio', return_value=0.5):
            with patch.object(analyzer, 'calculate_dividend_growth_rate', return_value=0.05):
                with patch.object(analyzer, 'get_dividend_streak', return_value=10):
                    with patch.object(analyzer, 'get_dividend_safety_score', return_value={
                        'ticker': 'AAPL',
                        'safety_score': 75,
                        'safety_grade': 'B',
                        'breakdown': {}
                    }):
                        metrics = analyzer.get_all_metrics('AAPL')
                        assert isinstance(metrics, dict)
                        assert 'payout_ratio' in metrics
                        assert 'dividend_growth_5y' in metrics
                        assert 'dividend_streak' in metrics
                        assert 'safety' in metrics
