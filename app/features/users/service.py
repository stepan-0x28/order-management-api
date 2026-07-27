from sqlalchemy.ext.asyncio import AsyncSession

from app.core.base.service import BaseService
from app.core.database.exceptions import UniqueViolationError, ForeignKeyViolationError

from app.security.passwords import hash_password, check_password
from app.security.auth.exceptions import IncorrectPasswordError

from app.features.users.repository import UserRepository
from app.features.users.model import User
from app.features.users.schemas import UserPersonal, UserIn
from app.features.users.exceptions import SameUsernameError, SamePasswordError, TakenUsernameError
from app.features.roles.exceptions import NonExistentRoleError
from app.features.roles.repository import RoleRepository


class UserService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

        self.__user_repository = UserRepository(session)
        self.__role_repository = RoleRepository(session)

    async def create(self, user_in: UserIn) -> int:
        if await self.__role_repository.get_by_id(user_in.role_id) is None:
            raise NonExistentRoleError

        if await self.__user_repository.get_by_username(user_in.username) is not None:
            raise TakenUsernameError

        user = User(
            username=user_in.username,
            password_hash=await hash_password(user_in.password),
            role_id=user_in.role_id,
            first_name=user_in.first_name,
            last_name=user_in.last_name
        )

        self.__user_repository.add(user)

        try:
            await self.flush()

            user_id = user.id

            await self.commit()
        except ForeignKeyViolationError:
            raise NonExistentRoleError
        except UniqueViolationError:
            raise TakenUsernameError

        return user_id

    async def update_personal(self, user: User, user_personal: UserPersonal):
        await self.__user_repository.update_personal(user.id, user_personal.first_name, user_personal.last_name)

        await self.commit()

    async def change_username(self, user: User, username: str):
        if username == user.username:
            raise SameUsernameError

        if await self.__user_repository.get_by_username(username) is not None:
            raise TakenUsernameError

        await self.__user_repository.update_username(user.id, username)

        try:
            await self.commit()
        except UniqueViolationError:
            raise TakenUsernameError

    async def change_password(self, user: User, current_password: str, new_password: str):
        if current_password == new_password:
            raise SamePasswordError

        if not await check_password(current_password, user.password_hash):
            raise IncorrectPasswordError

        await self.__user_repository.update_password_hash(user.id, await hash_password(new_password))

        await self.__user_repository.increase_token_version(user.id)

        await self.commit()
