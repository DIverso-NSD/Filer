from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
import jwt
from filler.core.schemas import User
from filler.core.settings import settings

token_scheme = APIKeyHeader(name="Token", auto_error=False)


async def verify_token(token: str = Depends(token_scheme)):
    if not token:
        raise HTTPException(403, {"error": "Ошибка доступа"})

    try:
        data = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        user_id = data["sub"]["user_id"]
        user_login = data["sub"]["user_login"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(403, {"error": "Истёкшая сессия"})
    except (jwt.InvalidTokenError, KeyError):
        raise HTTPException(403, {"error": "Ошибка доступа"})
    except Exception:
        raise HTTPException(500, {"error": "Server error"})

    return User(id=user_id, login=user_login)
