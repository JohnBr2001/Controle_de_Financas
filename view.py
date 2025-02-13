from models import Conta, engine, Bancos, Status, Historico, Tipos
from sqlmodel import Session, select
from datetime import date, timedelta
import matplotlib.pyplot as plt


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
        if conta.valor > 0:
            raise ValueError('Ainda há saldo disponivel nessa conta')
        conta.status = Status.INATIVO
        session.commit()


def transferir_saldo(id_conta_saida, id_conta_entrada, valor):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id == id_conta_saida)
        conta_saida = session.exec(statement).first()
        if conta_saida.valor < valor:
            raise ValueError("Saldo insuficiente")
        statement = select(Conta).where(Conta.id == id_conta_entrada)
        conta_entrada = session.exec(statement).first()

        conta_saida.valor = conta_saida.valor - valor
        conta_entrada.valor = conta_entrada.valor + valor
        session.commit()


def movimentar_dinheiro(historico: Historico):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id == historico.conta_id)
        conta = session.exec(statement).first()

        if Conta.status == Status.INATIVO:
            raise ValueError('Conta esta inativa')
            

        if historico.tipo == Tipos.ENTRADA:
            conta.valor += historico.valor
        else:
            if conta.valor < historico.valor:
                raise ValueError("Saldo insuficiente")
            conta.valor -= historico.valor

        session.add(historico)
        session.commit()
        return historico


def total_contas():
    with Session(engine) as session:
        statement = select(Conta)
        contas = session.exec(statement).all()

    total = 0
    for conta in contas:
        total += conta.valor
    return float(total)


def buscar_historico_entre_datas(data_inicio: date, data_fim: date):
    with Session(engine) as session:
        statement = select(Historico).where(
            Historico.data >= data_inicio, Historico.data <= data_fim)
        results = session.exec(statement).all()

        return results


def criar_grafico_por_conta():
    with Session(engine) as session:
        statement = select(Conta).where(Conta.status == Status.ATIVO)
        contas = session.exec(statement).all()
        bancos = []
        for i in contas:
            bancos.append(i.banco.value)

        total = []
        for i in contas:
            total.append(i.valor)



# criar_grafico_por_conta()
# x = buscar_historico_entre_datas(
# date.today() - timedelta(days=1), date.today() + timedelta(days=1))

# print(x)

# transferir_saldo(3, 1, 9)
# conta = Conta(valor=9, banco=Bancos.INTER)
# criar_conta(conta)
# print(listar_contas())
# desativar_conta(3)
"""  for i in listar_contas():
    print(i.banco)  """
# print(total_contas())
