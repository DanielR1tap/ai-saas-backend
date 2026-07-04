from datetime import UTC, datetime

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.tenant import Tenant
from backend.app.models.usage_event import UsageEvent


class UsageRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def reserve_credits(self, tenant_id: int, credits: int) -> bool:
        tenant = await self.session.get(Tenant, tenant_id)
        if tenant is None:
            return False

        used_credits = await self._current_month_credits(tenant_id)
        return used_credits + credits <= tenant.monthly_credit_limit

    async def commit_usage(self, tenant_id: int, credits: int, provider: str, model: str) -> None:
        self.session.add(
            UsageEvent(
                tenant_id=tenant_id,
                credits=credits,
                provider=provider,
                model=model,
            )
        )
        await self.session.commit()

    async def _current_month_credits(self, tenant_id: int) -> int:
        now = datetime.now(UTC)
        month_start = datetime(now.year, now.month, 1)
        statement: Select[tuple[int | None]] = select(func.sum(UsageEvent.credits)).where(
            UsageEvent.tenant_id == tenant_id,
            UsageEvent.created_at >= month_start,
        )
        result = await self.session.execute(statement)
        return result.scalar_one() or 0
