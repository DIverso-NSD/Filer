from fastapi import Depends
from fastapi.security import APIKeyHeader

from filler.core.schemas import User

token_scheme = APIKeyHeader(name="Token", auto_error=False)


async def verify_token(token: str = Depends(token_scheme)):
    return User(id=1, login="kuder")
