# noinspection PyPackageRequirements
import bcrypt
import asyncio


def _hash_password_sync(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def _check_password_sync(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))


async def hash_password(password: str) -> str:
    return await asyncio.to_thread(_hash_password_sync, password)


async def check_password(password: str, password_hash: str) -> bool:
    return await asyncio.to_thread(_check_password_sync, password, password_hash)
