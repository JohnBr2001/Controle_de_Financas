from models import Conta, engine, Bancos, Status
from sqlmodel import Session, select


def criar_conta(conta: Conta):
    with Session(engine) as session:

        statement = select(Conta).where(Conta.banco == conta.banco)
        results = session.exec(statement).all()

        if results:
            print('Ja existe uma conta nesse banco!')
            return
        session.add(conta)
        session.commit()
        return conta


def listar_contas():
    with Session(engine) as session:
        statement = select(Conta)
        results = session.exec(statement).all()
    return results


def desativar_conta(id):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id == id)
        """ Foi utilizado o first por ele trazer direto os dados do banco pelo id """
        conta = session.exec(statement).first()
        if conta.valor>0:
            raise ValueError('Ainda há saldo disponivel nessa conta')
        conta.status = Status.INATIVO
        session.commit()


#conta = Conta(valor=15, banco=Bancos.SANTANDER)
#criar_conta(conta)
#print(listar_contas())
desativar_conta(1)
""" for i in listar_contas():
    print(i.banco) """
