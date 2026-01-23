"""
Configuration Management
"""

import os


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-prod')

    # LLM settings
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    LLM_MODEL = 'claude-sonnet-4-20250514'
    LLM_MAX_TOKENS = 2000

    # RAG settings
    CHROMA_PERSIST_DIR = 'data/chroma'
    CORPUS_DIR = 'app/corpus'
    EMBEDDING_MODEL = 'all-MiniLM-L6-v2'
    RAG_TOP_K = 5

    # Backtest settings
    CODE_TIMEOUT_SECONDS = 10
    MAX_BACKTEST_YEARS = 10

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False

config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}