from datetime import datetime, UTC, timedelta
# noinspection PyPackageRequirements
from jose import jwt
# noinspection PyPackageRequirements
from jose.exceptions import JWTError
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.core.settings import settings

from app.security.passwords import check_password
from app.security.auth.exceptions import IncorrectUsernameOrPasswordError, NonExistentUserOrTokenExpiredError

from app.features.users.repository import UserRepository
from app.features.users.model import User


class AuthService:
    def __init__(self, session: AsyncSession):
        self.__user_repository = UserRepository(session)

    @staticmethod
    def __encode_token(user_id: int, token_version: int) -> str:
        now = datetime.now(UTC)

        claims = {
            'sub': str(user_id),
            'ver': token_version,
            'iat': int(now.timestamp()),
            'exp': int((now + timedelta(days=7)).timestamp())
        }

        return jwt.encode(claims, settings.token_signing_key)

    @staticmethod
    def __decode_token(token: str) -> tuple[int, int]:
        try:
            payload = jwt.decode(token, settings.token_signing_key)

            user_id = int(payload['sub'])
            token_version = int(payload['ver'])
        except (JWTError, KeyError, ValueError):
            raise NonExistentUserOrTokenExpiredError

        return user_id, token_version

    async def create_token(self, username: str, password: str) -> str:
        user = await self.__user_repository.get_by_username(username)

        if user is None:
            raise IncorrectUsernameOrPasswordError

        if not await check_password(password, user.password_hash):
            raise IncorrectUsernameOrPasswordError

        return self.__encode_token(user.id, user.token_version)

    async def get_user(self, token: str) -> User:
        user_id, token_version = self.__decode_token(token)

        user = await self.__user_repository.get_by_id(user_id)

        if user is None:
            raise NonExistentUserOrTokenExpiredError

        if user.token_version > token_version:
            raise NonExistentUserOrTokenExpiredError

        return user
