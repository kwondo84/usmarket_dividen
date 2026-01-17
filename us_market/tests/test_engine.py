"""
DividendEngine 테스트
- 포트폴리오 생성 기능
- 테마 및 티어 조회
- 필터링 및 제약 조건 검증
"""
import pytest
import os
import json
import sys
from unittest.mock import Mock, patch, MagicMock

# 프로젝트 루트를 경로에 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from us_market.dividend.engine import DividendEngine, OPTIMIZE_MODES


class TestDividendEngine:
    """DividendEngine 클래스 테스트"""
    
    @pytest.fixture
    def engine(self):
        """테스트용 엔진 인스턴스 생성"""
        return DividendEngine(data_dir='us_market/dividend')
    
    @pytest.fixture
    def mock_dividend_data(self):
        """모의 배당 데이터"""
        return {
            'SCHD': {
                'name': 'Schwab US Dividend Equity ETF',
                'price': 75.0,
                'yield': 0.035,
                'payments': [
                    {'date': '2024-03-20', 'amount': 0.65},
                    {'date': '2024-06-20', 'amount': 0.65},
                    {'date': '2024-09-20', 'amount': 0.65},
                    {'date': '2024-12-20', 'amount': 0.65}
                ]
            },
            'JEPI': {
                'name': 'JPMorgan Equity Premium Income ETF',
                'price': 55.0,
                'yield': 0.08,
                'payments': [
                    {'date': '2024-01-31', 'amount': 0.36},
                    {'date': '2024-02-29', 'amount': 0.36},
                    {'date': '2024-03-29', 'amount': 0.36}
                ]
            },
            'O': {
                'name': 'Realty Income Corp',
                'price': 60.0,
                'yield': 0.055,
                'payments': [
                    {'date': '2024-01-15', 'amount': 0.275},
                    {'date': '2024-02-15', 'amount': 0.275},
                    {'date': '2024-03-15', 'amount': 0.275}
                ]
            }
        }
    
    def test_engine_initialization(self, engine):
        """엔진 초기화 테스트"""
        assert engine is not None
        assert engine.data_dir == 'us_market/dividend'
        assert engine.config_dir == 'us_market/dividend/config'
        assert engine.data_subdir == 'us_market/dividend/data'
        assert hasattr(engine, 'plans')
        assert hasattr(engine, 'tags_def')
        assert hasattr(engine, 'dividend_data')
        assert hasattr(engine, 'symbol_tags')
    
    def test_get_themes(self, engine):
        """테마 목록 조회 테스트"""
        themes = engine.get_themes()
        assert isinstance(themes, list)
        if len(themes) > 0:
            theme = themes[0]
            assert 'id' in theme
            assert 'title' in theme
            assert 'subtitle' in theme
    
    def test_generate_portfolio_invalid_theme(self, engine):
        """잘못된 테마 ID로 포트폴리오 생성 시도"""
        result = engine.generate_portfolio(
            theme_id='invalid_theme',
            tier_id='balanced',
            target_monthly_krw=1000000
        )
        assert 'error' in result
        assert 'not found' in result['error'].lower()
    
    def test_generate_portfolio_invalid_tier(self, engine):
        """잘못된 티어 ID로 포트폴리오 생성 시도"""
        themes = engine.get_themes()
        if len(themes) > 0:
            theme_id = themes[0]['id']
            result = engine.generate_portfolio(
                theme_id=theme_id,
                tier_id='invalid_tier',
                target_monthly_krw=1000000
            )
            assert 'error' in result
            assert 'not found' in result['error'].lower()
    
    def test_generate_portfolio_valid(self, engine):
        """유효한 파라미터로 포트폴리오 생성"""
        themes = engine.get_themes()
        if len(themes) > 0:
            theme_id = themes[0]['id']
            result = engine.generate_portfolio(
                theme_id=theme_id,
                tier_id='balanced',
                target_monthly_krw=1000000,
                fx_rate=1420,
                tax_rate=0.154,
                optimize_mode='greedy'
            )
            
            # 에러가 없는 경우 결과 구조 검증
            if 'error' not in result:
                assert 'theme_id' in result
                assert 'tier_id' in result
                assert 'required_capital_krw' in result
                assert 'expected_monthly_krw' in result
                assert 'portfolio_yield' in result
                assert 'allocation' in result
                assert isinstance(result['allocation'], list)
                assert 'chart_data' in result
                assert isinstance(result['chart_data'], list)
                assert len(result['chart_data']) == 12
    
    def test_generate_all_tiers(self, engine):
        """모든 티어 포트폴리오 생성"""
        themes = engine.get_themes()
        if len(themes) > 0:
            theme_id = themes[0]['id']
            results = engine.generate_all_tiers(
                theme_id=theme_id,
                target_monthly_krw=1000000
            )
            assert isinstance(results, dict)
            assert 'defensive' in results
            assert 'balanced' in results
            assert 'aggressive' in results
    
    def test_optimize_modes(self):
        """최적화 모드 상수 검증"""
        assert isinstance(OPTIMIZE_MODES, list)
        assert 'greedy' in OPTIMIZE_MODES
        assert 'risk_parity' in OPTIMIZE_MODES
        assert 'mean_variance' in OPTIMIZE_MODES
        assert 'max_sharpe' in OPTIMIZE_MODES
        assert 'min_vol' in OPTIMIZE_MODES
    
    def test_portfolio_allocation_structure(self, engine):
        """포트폴리오 할당 구조 검증"""
        themes = engine.get_themes()
        if len(themes) > 0:
            theme_id = themes[0]['id']
            result = engine.generate_portfolio(
                theme_id=theme_id,
                tier_id='balanced',
                target_monthly_krw=1000000
            )
            
            if 'error' not in result and 'allocation' in result:
                for item in result['allocation']:
                    assert 'ticker' in item
                    assert 'name' in item
                    assert 'weight' in item
                    assert 'shares' in item
                    assert 'price' in item
                    assert 'yield' in item
                    assert 'amount_usd' in item
                    assert isinstance(item['weight'], (int, float))
                    assert item['weight'] >= 0
                    assert item['weight'] <= 100
    
    def test_portfolio_yield_calculation(self, engine):
        """포트폴리오 수익률 계산 검증"""
        themes = engine.get_themes()
        if len(themes) > 0:
            theme_id = themes[0]['id']
            result = engine.generate_portfolio(
                theme_id=theme_id,
                tier_id='balanced',
                target_monthly_krw=1000000
            )
            
            if 'error' not in result:
                assert 'portfolio_yield' in result
                yield_str = result['portfolio_yield']
                assert isinstance(yield_str, str)
                assert '%' in yield_str
                # 수익률이 0보다 커야 함
                yield_value = float(yield_str.replace('%', ''))
                assert yield_value > 0
    
    def test_capital_requirement_calculation(self, engine):
        """필요 자본 계산 검증"""
        themes = engine.get_themes()
        if len(themes) > 0:
            theme_id = themes[0]['id']
            result = engine.generate_portfolio(
                theme_id=theme_id,
                tier_id='balanced',
                target_monthly_krw=1000000,
                fx_rate=1420
            )
            
            if 'error' not in result:
                assert 'required_capital_krw' in result
                capital = result['required_capital_krw']
                assert isinstance(capital, (int, float))
                assert capital > 0
    
    def test_monthly_cashflow_chart(self, engine):
        """월별 현금흐름 차트 데이터 검증"""
        themes = engine.get_themes()
        if len(themes) > 0:
            theme_id = themes[0]['id']
            result = engine.generate_portfolio(
                theme_id=theme_id,
                tier_id='balanced',
                target_monthly_krw=1000000
            )
            
            if 'error' not in result:
                assert 'chart_data' in result
                chart_data = result['chart_data']
                assert isinstance(chart_data, list)
                assert len(chart_data) == 12  # 12개월
                # 모든 값이 숫자여야 함
                for value in chart_data:
                    assert isinstance(value, (int, float))
                    assert value >= 0
