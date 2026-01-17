"""
pytest 설정 파일
공통 픽스처 및 설정
"""
import pytest
import sys
import os

# 프로젝트 루트를 경로에 추가
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.insert(0, project_root)

@pytest.fixture(scope="session")
def test_data_dir():
    """테스트 데이터 디렉토리 경로"""
    return os.path.join(project_root, 'us_market', 'dividend', 'data')

@pytest.fixture(scope="session")
def test_config_dir():
    """테스트 설정 디렉토리 경로"""
    return os.path.join(project_root, 'us_market', 'dividend', 'config')
