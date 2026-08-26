import os

# Set before any test module (e.g. test_routes) imports `main`, since that
# import evaluates Settings() at module load time.
os.environ.setdefault("MODEL_NAME", "test-model")
os.environ.setdefault("USE_STUB_PROVIDER", "true")
os.environ.setdefault("ENABLE_ENRICHMENT", "false")
os.environ.setdefault("ALLOWED_ORIGINS", "http://localhost:5173")

import pytest

from core.config import get_settings


@pytest.fixture(autouse=True)
def _reset_settings_cache():
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()
