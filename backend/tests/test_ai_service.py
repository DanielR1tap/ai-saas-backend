import pytest

from backend.app.services.ai_service import AiService, MockAiProvider


@pytest.mark.asyncio
async def test_mock_ai_provider_returns_text() -> None:
    service = AiService(provider=MockAiProvider())

    result = await service.complete(prompt="Write a tagline")

    assert result.provider == "mock"
    assert "Write a tagline" in result.text
