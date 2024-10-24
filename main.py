from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from models import SessionLocal, Pessoa, PessoaCreate, PessoaResponse

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/pessoas/", response_model=PessoaResponse)
def create_pessoa(pessoa: PessoaCreate, db: Session = Depends(get_db)):
    db_pessoa = Pessoa(**pessoa.dict())
    db.add(db_pessoa)
    db.commit()
    db.refresh(db_pessoa)
    return db_pessoa

@app.get("/pessoas/{pessoa_id}", response_model=PessoaResponse)
def read_pessoa(pessoa_id: int, db: Session = Depends(get_db)):
    db_pessoa = db.query(Pessoa).filter(Pessoa.id == pessoa_id).first()
    if db_pessoa is None:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
    return db_pessoa

@app.put("/pessoas/{pessoa_id}", response_model=PessoaResponse)
def update_pessoa(pessoa_id: int, pessoa: PessoaCreate, db: Session = Depends(get_db)):
    db_pessoa = db.query(Pessoa).filter(Pessoa.id == pessoa_id).first()
    if db_pessoa is None:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
    for key, value in pessoa.dict().items():
        setattr(db_pessoa, key, value)
    db.commit()
    db.refresh(db_pessoa)
    return db_pessoa

@app.delete("/pessoas/{pessoa_id}")
def delete_pessoa(pessoa_id: int, db: Session = Depends(get_db)):
    db_pessoa = db.query(Pessoa).filter(Pessoa.id == pessoa_id).first()
    if db_pessoa is None:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
    db.delete(db_pessoa)
    db.commit()
    return {"message": "Pessoa excluída com sucesso"}
