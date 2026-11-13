from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas  # noqa: F401
from app.database import Base, engine, get_db

app = FastAPI(title="Sistema de Academia")


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "API da academia funcionando"}

@app.post("/alunos/", response_model=schemas.AlunoRead)
def criar_aluno(aluno: schemas.AlunoCreate, db: Session = Depends(get_db)):
    db_aluno = models.Aluno(**aluno.model_dump())
    db.add(db_aluno)
    db.commit()
    db.refresh(db_aluno)
    return db_aluno


@app.get("/alunos/", response_model=list[schemas.AlunoRead])
def listar_alunos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Aluno).offset(skip).limit(limit).all()


@app.post("/matriculas/", response_model=schemas.MatriculaRead)
def criar_matricula(matricula: schemas.MatriculaCreate, db: Session = Depends(get_db)):
    aluno = db.query(models.Aluno).filter(models.Aluno.id == matricula.aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    db_matricula = models.Matricula(**matricula.model_dump())
    db.add(db_matricula)
    db.commit()
    db.refresh(db_matricula)
    return db_matricula


@app.get("/matriculas/", response_model=list[schemas.MatriculaRead])
def listar_matriculas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Matricula).offset(skip).limit(limit).all()


@app.post("/pagamentos/", response_model=schemas.PagamentoRead)
def registrar_pagamento(pagamento: schemas.PagamentoCreate, db: Session = Depends(get_db)):
    matricula = db.query(models.Matricula).filter(models.Matricula.id == pagamento.matricula_id).first()
    if not matricula:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada")

    db_pagamento = models.Pagamento(**pagamento.model_dump())
    db.add(db_pagamento)
    db.commit()
    db.refresh(db_pagamento)
    return db_pagamento


@app.get("/pagamentos/", response_model=list[schemas.PagamentoRead])
def listar_pagamentos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Pagamento).offset(skip).limit(limit).all()
