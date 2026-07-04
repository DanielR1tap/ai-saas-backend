from backend.app.core.security import create_access_token, decode_access_token


def test_access_token_roundtrip() -> None:
    token = create_access_token(subject="123")

    payload = decode_access_token(token)

    assert payload["sub"] == "123"
