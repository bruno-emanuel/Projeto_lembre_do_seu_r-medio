from itsdangerous import URLSafeSerializer

SECRET_KEY = "chave-super-secreta-lembremed"
serializer = URLSafeSerializer(SECRET_KEY, salt="auth")

def criar_token(user_id: int):
    return serializer.dumps({"user_id": user_id})

def ler_token(token: str):
    try:
        dados = serializer.loads(token)
        return dados.get("user_id")
    except Exception:
        return None
