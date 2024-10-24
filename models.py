from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from datetime import date

DATABASE_URL = "mysql+pymysql://root:20102008@localhost/empresa"  # Altere para suas credenciais

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Pessoa(Base):
    __tablename__ = 'pessoas'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    data_nascimento = Column(Date)
    endereco = Column(String)
    cpf = Column(String, unique=True)
    estado_civil = Column(String)

# Pydantic model for request and response
class PessoaCreate(BaseModel):
    nome: str
    data_nascimento: date
    endereco: str
    cpf: str
    estado_civil: str

    class Config:
        orm_mode = True

class PessoaResponse(BaseModel):
    id: int
    nome: str
    data_nascimento: date
    endereco: str
    cpf: str
    estado_civil: str

    class Config:
        from_attributes = True

Base.metadata.create_all(bind=engine)
