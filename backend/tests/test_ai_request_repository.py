from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest

from backend.app.services.ai_request_repository import AiRequestRepository


@pytest.mark.asyncio
async def test_create_ai_request_flushes_and_refreshes() -> None:
    session = SimpleNamespace(
        add=Mock(),
        flush=AsyncMock(),
        refresh=AsyncMock(),
    )
    session.refresh.side_effect = lambda ai_request: setattr(ai_request, "id", 1)
    repository = AiRequestRepository(session)

    ai_request = await repository.create(
        tenant_id=10,
        user_id=20,
        prompt="Summarize this",
        system=None,
        response_text="Short summary",
        provider="mock",
        ai_model="mock-local",
        credits=1,
    )

    session.add.assert_called_once()
    session.flush.assert_awaited_once()
    session.refresh.assert_awaited_once()
    assert ai_request.id == 1
    assert ai_request.tenant_id == 10
    assert ai_request.user_id == 20
    assert ai_request.response_text == "Short summary"
