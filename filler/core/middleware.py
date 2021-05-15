from fastapi import Depends
from fastapi.security import APIKeyHeader
import jwt

from filler.core.schemas import User
from filler.core.settings import settings

token_scheme = APIKeyHeader(name="Token", auto_error=False)


async def verify_token(token: str = Depends(token_scheme)):
    print(token)
    print(settings.secret_key)

    data = jwt.decode(token, settings.secret_key, algorithms=["HS256"])

    return User(id=1, login="kuder")
