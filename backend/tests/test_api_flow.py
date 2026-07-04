import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_login_and_read_current_user(api_client: AsyncClient) -> None:
    register_response = await api_client.post(
        "/api/v1/auth/register",
        json={
            "organization_name": "Acme AI",
            "email": "owner@example.com",
            "password": "strong-password",
        },
    )

    assert register_response.status_code == 201
    register_payload = register_response.json()
    assert register_payload["token_type"] == "bearer"
    assert register_payload["access_token"]

    login_response = await api_client.post(
        "/api/v1/auth/login",
        data={
            "username": "owner@example.com",
            "password": "strong-password",
        },
    )

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    me_response = await api_client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert me_response.status_code == 200
    me_payload = me_response.json()
    assert me_payload["email"] == "owner@example.com"
    assert me_payload["role"] == "owner"


@pytest.mark.asyncio
async def test_ai_completion_is_saved_to_history(api_client: AsyncClient) -> None:
    register_response = await api_client.post(
        "/api/v1/auth/register",
        json={
            "organization_name": "Acme AI",
            "email": "ai-user@example.com",
            "password": "strong-password",
        },
    )
    token = register_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    completion_response = await api_client.post(
        "/api/v1/ai/complete",
        headers=headers,
        json={
            "prompt": "Write a short SaaS tagline",
            "system": "You are concise.",
            "estimated_credits": 2,
        },
    )

    assert completion_response.status_code == 200
    completion_payload = completion_response.json()
    assert completion_payload["request_id"]
    assert completion_payload["provider"] == "mock"
    assert completion_payload["used_credits"] == 2

    history_response = await api_client.get("/api/v1/ai/requests", headers=headers)

    assert history_response.status_code == 200
    history_payload = history_response.json()
    assert len(history_payload) == 1
    assert history_payload[0]["id"] == completion_payload["request_id"]
    assert history_payload[0]["prompt"] == "Write a short SaaS tagline"
    assert history_payload[0]["credits"] == 2
