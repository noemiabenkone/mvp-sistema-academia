from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class AlunoBase(BaseModel):
    nome: str = Field(..., min_length=2)
    cpf: str = Field(..., min_length=11, max_length=11)
    telefone: Optional[str] = None


class AlunoCreate(AlunoBase):
    pass


class AlunoRead(AlunoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class MatriculaBase(BaseModel):
    plano: str
    status: str = "Ativo"


class MatriculaCreate(MatriculaBase):
    aluno_id: int


class MatriculaRead(MatriculaBase):
    id: int
    aluno_id: int
    data_inicio: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


class PagamentoBase(BaseModel):
    valor: float
    status_pagamento: str = "Pendente"


class PagamentoCreate(PagamentoBase):
    matricula_id: int


class PagamentoRead(PagamentoBase):
    id: int
    matricula_id: int
    data_pagamento: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)
