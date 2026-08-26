from core.config import Settings
from services.providers.base import TextGenerator
from services.providers.openai_provider import OpenAIProvider
from services.providers.stub_provider import StubProvider


def build_provider(settings: Settings) -> TextGenerator:
    if settings.USE_STUB_PROVIDER:
        return StubProvider()
    return OpenAIProvider(
        api_key=settings.PROVIDER_API_KEY,
        base_url=settings.PROVIDER_BASE_URL,
        model=settings.MODEL_NAME,
        timeout=settings.REQUEST_TIMEOUT,
    )
