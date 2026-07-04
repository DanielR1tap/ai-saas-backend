from sqlalchemy import Select, desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.ai_request import AiRequest


class AiRequestRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        tenant_id: int,
        user_id: int,
        prompt: str,
        system: str | None,
        response_text: str,
        provider: str,
        ai_model: str,
        credits: int,
    ) -> AiRequest:
        ai_request = AiRequest(
            tenant_id=tenant_id,
            user_id=user_id,
            prompt=prompt,
            system=system,
            response_text=response_text,
            provider=provider,
            ai_model=ai_model,
            credits=credits,
        )
        self.session.add(ai_request)
        await self.session.flush()
        await self.session.refresh(ai_request)
        return ai_request

    async def list_for_tenant(self, tenant_id: int, limit: int = 50) -> list[AiRequest]:
        statement: Select[tuple[AiRequest]] = (
            select(AiRequest)
            .where(AiRequest.tenant_id == tenant_id)
            .order_by(desc(AiRequest.created_at))
            .limit(limit)
        )
        result = await self.session.execute(statement)
        return list(result.scalars().all())
