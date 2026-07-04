from backend.app.services.usage_service import UsageService


def test_usage_service_blocks_after_limit() -> None:
    service = UsageService()

    assert service.reserve_credits("tenant-a", 100)
    service.commit_usage("tenant-a", 100, provider="mock", model="mock-local")

    assert not service.reserve_credits("tenant-a", 1)
