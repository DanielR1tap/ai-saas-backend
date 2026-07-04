from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest

from backend.app.schemas.auth import RegisterRequest
from backend.app.services.auth_service import AuthService


@pytest.mark.asyncio
async def test_register_owner_creates_tenant_and_user() -> None:
    session = SimpleNamespace(
        add=Mock(),
        flush=AsyncMock(),
        commit=AsyncMock(),
        refresh=AsyncMock(),
    )
    session.refresh.side_effect = lambda user: setattr(user, "id", 1)

    service = AuthService(session)
    payload = RegisterRequest(
        organization_name="Acme AI",
        email="OWNER@EXAMPLE.COM",
        password="strong-password",
    )

    token = await service.register_owner(payload)

    added_objects = [call.args[0] for call in session.add.call_args_list]
    tenant = added_objects[0]
    user = added_objects[1]

    assert tenant.name == "Acme AI"
    assert user.email == "owner@example.com"
    assert token.token_type == "bearer"
    assert token.access_token
