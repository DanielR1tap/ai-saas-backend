from dataclasses import dataclass
from typing import Protocol

from backend.app.core.config import settings


@dataclass(frozen=True)
class AiResult:
    text: str
    provider: str
    model: str


class AiProvider(Protocol):
    async def complete(self, prompt: str, system: str | None = None) -> AiResult:
        pass


class MockAiProvider:
    async def complete(self, prompt: str, system: str | None = None) -> AiResult:
        prefix = f"{system.strip()} " if system else ""
        return AiResult(
            text=f"{prefix}Mock AI response for: {prompt}",
            provider="mock",
            model="mock-local",
        )


class OpenAiProvider:
    def __init__(self, api_key: str, model: str) -> None:
        self.api_key = api_key
        self.model = model

    async def complete(self, prompt: str, system: str | None = None) -> AiResult:
        from openai import AsyncOpenAI

        client = AsyncOpenAI(api_key=self.api_key)
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = await client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        text = response.choices[0].message.content or ""
        return AiResult(text=text, provider="openai", model=self.model)


class AiService:
    def __init__(self, provider: AiProvider) -> None:
        self.provider = provider

    async def complete(self, prompt: str, system: str | None = None) -> AiResult:
        return await self.provider.complete(prompt=prompt, system=system)


def build_ai_provider() -> AiProvider:
    provider_name = settings.ai_provider.lower()
    if provider_name == "openai":
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is required when AI_PROVIDER=openai.")
        return OpenAiProvider(api_key=settings.openai_api_key, model=settings.ai_model)
    return MockAiProvider()


def get_ai_service() -> AiService:
    return AiService(provider=build_ai_provider())
