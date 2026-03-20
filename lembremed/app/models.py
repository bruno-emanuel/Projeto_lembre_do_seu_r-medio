from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    senha = Column(String, nullable=False)

    idosos = relationship("Idoso", back_populates="usuario", cascade="all, delete")

class Idoso(Base):
    __tablename__ = "idosos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    idade = Column(Integer, nullable=False)
    telefone = Column(String, nullable=False)
    cuidador_nome = Column(String, nullable=True)
    cuidador_telefone = Column(String, nullable=True)
    observacoes = Column(Text, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    usuario = relationship("User", back_populates="idosos")
    remedios = relationship("Remedio", back_populates="idoso", cascade="all, delete")

class Remedio(Base):
    __tablename__ = "remedios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    dose = Column(String, nullable=False)
    horario = Column(String, nullable=False)
    frequencia = Column(String, nullable=False)
    instrucoes = Column(Text, nullable=True)

    idoso_id = Column(Integer, ForeignKey("idosos.id"), nullable=False)

    idoso = relationship("Idoso", back_populates="remedios")
    historicos = relationship("Historico", back_populates="remedio", cascade="all, delete")

class Historico(Base):
    __tablename__ = "historicos"

    id = Column(Integer, primary_key=True, index=True)
    remedio_id = Column(Integer, ForeignKey("remedios.id"), nullable=False)
    data_hora = Column(DateTime, default=datetime.now)
    status = Column(String, nullable=False)
    observacao = Column(Text, nullable=True)

    remedio = relationship("Remedio", back_populates="historicos")
