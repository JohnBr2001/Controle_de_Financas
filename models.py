from sqlmodel import SQLModel, Field, create_engine, Relationship
from enum import Enum
from datetime import date


""" create_engine <--Cria o banco de dados 
    Field <-- Especica coisas dentro do campo

"""

""" Utilizamos o Enum para dar apenas algumas opções restritas que o usuario pode selecionar(ou seja lista a posibilidades que o usuario pode selecionar) """


class Bancos(Enum):
    NUBANK = 'Nubank'
    SANTANDER = 'Santander'
    INTER = 'Inter'
    BRADESCO = 'Bradesco'
    ITAU = 'Itau'
    SAFRA = 'Safra'


class Status(Enum):
    ATIVO = 'Ativo'
    INATIVO = 'Inativo'
    EM_IMPLANTACAO = 'IMPLANTANDO'


class Tipos(Enum):

    ENTRADA = 'Entrada'
    SAIDA = 'Saida'


""" Criando a class conta dentro dela existe a tabela onde contem os campos que vamos trabalhar """


class Conta(SQLModel, table=True):
    """ primary_key garante que nunca se repita os dados """
    id: int = Field(primary_key=True)
    valor: float
    banco: Bancos = Field(default=Bancos.NUBANK)
    status: Status = Field(default=Status.ATIVO)


class Historico(SQLModel, table=True):
    id: int = Field(primary_key=True)
    conta_id: int = Field(foreign_key="conta.id")
    conta: Conta = Relationship()
    tipo: Tipos = Field(default=Tipos.ENTRADA)
    valor: float
    data: date


""" Aqui estamos definitivamente informando ao Python que ele deve criar um banco de dados com as informações fornecidas, passamos o nome do banco e qual tipo de banco vamos usar: no caso SQLlite """

sqlite_file_name = 'database.db'
sqlite_url = f"sqlite:///{sqlite_file_name}"

""" Deixamos os echo como True para enquanto estamos reliazando o desenvolimento da aplicação ele mostrar todo os erros ou todas as informações, apos terminar a aplicação podemos colocar como false """

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()
