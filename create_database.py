import pymysql
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError

# Configurações do banco de dados
host = 'localhost'
user = 'root'  # seu usuário do MySQL
password = '20102008'  # sua senha do MySQL
db_name = 'empresa'  # nome do banco de dados que você quer criar

connection = pymysql.connect(host=host, user=user, password=password)

try:
    with connection.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
        print(f"Banco de dados '{db_name}' criado ou já existe.")
finally:
    connection.close()

engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{db_name}")

try:
    with engine.connect() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS pessoas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome_completo VARCHAR(100) NOT NULL,
                data_nascimento DATE NOT NULL,
                endereco VARCHAR(200),
                cpf VARCHAR(11) NOT NULL UNIQUE,
                estado_civil VARCHAR(20)
            );
        """))
        print("Tabela 'pessoas' criada ou já existe.")
except ProgrammingError as e:
    print(f"Erro ao criar a tabela: {e}")
