from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, unique=True, index=True, nullable=False)
    telefone = Column(String, nullable=True)

    matriculas = relationship("Matricula", back_populates="aluno")

class Matricula(Base):
    __tablename__ = "matriculas"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
    plano = Column(String, nullable=False)
    data_inicio = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="Ativo")

    aluno = relationship("Aluno", back_populates="matriculas")
    pagamentos = relationship("Pagamento", back_populates="matricula")

class Pagamento(Base):
    __tablename__ = "pagamentos"

    id = Column(Integer, primary_key=True, index=True)
    matricula_id = Column(Integer, ForeignKey("matriculas.id"), nullable=False)
    valor = Column(Float, nullable=False)
    status_pagamento = Column(String, default="Pendente") # Pendente ou Quitado
    data_pagamento = Column(DateTime, nullable=True)

    matricula = relationship("Matricula", back_populates="pagamentos")