from collections import defaultdict

from backend.app.core.config import settings


class UsageService:
    def __init__(self) -> None:
        self._monthly_usage: defaultdict[str, int] = defaultdict(int)

    def reserve_credits(self, tenant_id: str, credits: int) -> bool:
        current_usage = self._monthly_usage[tenant_id]
        return current_usage + credits <= settings.free_plan_monthly_credits

    def commit_usage(self, tenant_id: str, credits: int, provider: str, model: str) -> None:
        self._monthly_usage[tenant_id] += credits


usage_service = UsageService()


def get_usage_service() -> UsageService:
    return usage_service
