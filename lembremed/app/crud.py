from sqlalchemy.orm import Session
from . import models

def criar_usuario(db: Session, nome: str, email: str, senha: str):
    usuario = models.User(nome=nome, email=email, senha=senha)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

def buscar_usuario_por_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def criar_idoso(db: Session, dados: dict, user_id: int):
    idoso = models.Idoso(**dados, user_id=user_id)
    db.add(idoso)
    db.commit()
    db.refresh(idoso)
    return idoso

def listar_idosos(db: Session, user_id: int):
    return db.query(models.Idoso).filter(models.Idoso.user_id == user_id).all()

def listar_remedios(db: Session, user_id: int):
    return (
        db.query(models.Remedio)
        .join(models.Idoso)
        .filter(models.Idoso.user_id == user_id)
        .all()
    )

def listar_historico(db: Session, user_id: int):
    return (
        db.query(models.Historico)
        .join(models.Remedio)
        .join(models.Idoso)
        .filter(models.Idoso.user_id == user_id)
        .order_by(models.Historico.data_hora.desc())
        .all()
    )
