from fastapi import Request
from .auth import ler_token

def get_current_user_id(request: Request):
    token = request.cookies.get("token")
    if not token:
        return None
    return ler_token(token)
