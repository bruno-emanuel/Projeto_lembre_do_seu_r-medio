from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str

class IdosoCreate(BaseModel):
    nome: str
    idade: int
    telefone: str
    cuidador_nome: Optional[str] = None
    cuidador_telefone: Optional[str] = None
    observacoes: Optional[str] = None
