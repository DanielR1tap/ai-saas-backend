from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.config import settings
from backend.app.core.security import create_access_token, hash_password, verify_password
from backend.app.models.tenant import Tenant
from backend.app.models.user import User
from backend.app.schemas.auth import AuthToken, LoginRequest, RegisterRequest


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self.session.get(User, user_id)

    async def get_user_by_email(self, email: str) -> User | None:
        result = await self.session.execute(select(User).where(User.email == email.lower()))
        return result.scalar_one_or_none()

    async def register_owner(self, payload: RegisterRequest) -> AuthToken:
        tenant = Tenant(
            name=payload.organization_name,
            plan="free",
            monthly_credit_limit=settings.free_plan_monthly_credits,
        )
        self.session.add(tenant)
        await self.session.flush()

        user = User(
            tenant_id=tenant.id,
            email=payload.email.lower(),
            password_hash=hash_password(payload.password),
            role="owner",
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return self._issue_token(user)

    async def authenticate(self, payload: LoginRequest) -> AuthToken | None:
        user = await self.get_user_by_email(payload.email)
        if user is None:
            return None
        if not verify_password(payload.password, user.password_hash):
            return None
        return self._issue_token(user)

    def _issue_token(self, user: User) -> AuthToken:
        return AuthToken(access_token=create_access_token(subject=str(user.id)))
