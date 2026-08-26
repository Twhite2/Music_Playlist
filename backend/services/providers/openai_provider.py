import httpx

from services.providers.base import ProviderUnavailableError


class OpenAIProvider:
    """TextGenerator backed by OpenAI's chat completions endpoint. This is
    the only file that knows OpenAI's request/response shape."""

    def __init__(self, api_key: str, base_url: str, model: str, timeout: float):
        self._model = model
        self._client = httpx.AsyncClient(
            base_url=base_url,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=timeout,
        )

    async def generate(self, prompt: str) -> str:
        try:
            response = await self._client.post(
                "/chat/completions",
                json={
                    "model": self._model,
                    "messages": [{"role": "user", "content": prompt}],
                    "response_format": {"type": "json_object"},
                },
            )
            response.raise_for_status()
        except (httpx.TimeoutException, httpx.ConnectError, httpx.HTTPStatusError) as exc:
            raise ProviderUnavailableError(str(exc)) from exc

        return response.json()["choices"][0]["message"]["content"]
