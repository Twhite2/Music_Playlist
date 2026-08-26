from typing import Protocol


class TextGenerator(Protocol):
    async def generate(self, prompt: str) -> str: ...


class ProviderUnavailableError(Exception):
    """Raised when the text-generation provider cannot be reached or fails."""
