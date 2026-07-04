from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.dependencies import get_current_user
from backend.app.db import get_db_session
from backend.app.models.user import User
from backend.app.schemas.ai import AiCompletionRequest, AiCompletionResponse, AiRequestRead
from backend.app.services.ai_request_repository import AiRequestRepository
from backend.app.services.ai_service import AiService, get_ai_service
from backend.app.services.usage_repository import UsageRepository

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/complete", response_model=AiCompletionResponse)
async def complete_text(
    payload: AiCompletionRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
    ai_service: AiService = Depends(get_ai_service),
) -> AiCompletionResponse:
    usage_repository = UsageRepository(session)
    ai_request_repository = AiRequestRepository(session)
    allowed = await usage_repository.reserve_credits(
        tenant_id=current_user.tenant_id,
        credits=payload.estimated_credits,
    )
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Monthly AI credits exceeded for this tenant.",
        )

    result = await ai_service.complete(prompt=payload.prompt, system=payload.system)
    ai_request = await ai_request_repository.create(
        tenant_id=current_user.tenant_id,
        user_id=current_user.id,
        prompt=payload.prompt,
        system=payload.system,
        response_text=result.text,
        provider=result.provider,
        ai_model=result.model,
        credits=payload.estimated_credits,
    )
    await usage_repository.commit_usage(
        tenant_id=current_user.tenant_id,
        credits=payload.estimated_credits,
        provider=result.provider,
        model=result.model,
    )
    return AiCompletionResponse(
        request_id=ai_request.id,
        text=result.text,
        provider=result.provider,
        model=result.model,
        used_credits=payload.estimated_credits,
    )


@router.get("/requests", response_model=list[AiRequestRead])
async def list_ai_requests(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> list[AiRequestRead]:
    repository = AiRequestRepository(session)
    requests = await repository.list_for_tenant(current_user.tenant_id)
    return [AiRequestRead.model_validate(request) for request in requests]
