from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
import jwt
from filler.core.schemas import User
from filler.core.settings import settings

token_scheme = APIKeyHeader(name="Token", auto_error=False)


async def verify_token(token: str = Depends(token_scheme)):

    invalid_msg = {"error": "Ошибка доступа"}
    expired_msg = {"error": "Истёкшая сессия"}
    server_error = {"error": "Server error"}

    if token:
        try:
            data = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
            if 'sub' in data:
                user_id = data['sub']['user_id']
                user_login = data['sub']['user_login']

        except jwt.ExpiredSignatureError:
            code = 403
            raise HTTPException(code, expired_msg)
        except jwt.InvalidTokenError:
            code = 403
            raise HTTPException(code, invalid_msg)
        except Exception:
            code = 500
            raise HTTPException(code, server_error)



    return User(id=user_id, login=user_login)
