from app.core.database.exceptions import UniqueViolationError
from app.core.database.session import DBSessionWrapper

from app.security.passwords import hash_password, check_password
from app.security.auth.exceptions import IncorrectPasswordError

from app.features.users.repository import UserRepository
from app.features.users.model import User
from app.features.users.schemas import UserPersonal, UserIn
from app.features.users.exceptions import SameUsernameError, SamePasswordError, TakenUsernameError
from app.features.roles.exceptions import NonExistentRoleError
from app.features.roles.repository import RoleRepository


class UserService:
    def __init__(self, user_repository: UserRepository, role_repository: RoleRepository, db_session: DBSessionWrapper):
        self.__user_repository = user_repository
        self.__role_repository = role_repository

        self.__db_session = db_session

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

        self.__db_session.add(user)

        try:
            await self.__db_session.commit()
        except UniqueViolationError as err:
            if err.column == User.username:
                raise TakenUsernameError

        return user.id

    async def update_personal_data(self, user: User, user_personal: UserPersonal):
        user.first_name = user_personal.first_name
        user.last_name = user_personal.last_name

        await self.__db_session.commit()

    async def change_username(self, user: User, username: str):
        if username == user.username:
            raise SameUsernameError

        if await self.__user_repository.get_by_username(username) is not None:
            raise TakenUsernameError

        user.username = username

        try:
            await self.__db_session.commit()
        except UniqueViolationError as err:
            if err.column == User.username:
                raise TakenUsernameError

    async def change_password(self, user: User, current_password: str, new_password: str):
        if not await check_password(current_password, user.password_hash):
            raise IncorrectPasswordError

        if current_password == new_password:
            raise SamePasswordError

        user.password_hash = await hash_password(new_password)
        user.token_version += 1

        await self.__db_session.commit()
