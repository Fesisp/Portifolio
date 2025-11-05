from abc import ABC, abstractmethod
from datetime import datetime

DIAS_SEMANA_PT = [
    "segunda-feira", "terça-feira", "quarta-feira",
    "quinta-feira", "sexta-feira", "sábado", "domingo"
]

def formatar_data_pt(dt):
    dia_semana = DIAS_SEMANA_PT[dt.weekday()]
    return f"{dia_semana.capitalize()}, {dt.strftime('%d/%m/%Y %H:%M')}"

#CLASSES UML

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if self.valor > 0:
            conta.saldo += self.valor
            conta.historico.adicionar_transacao(
                f"{formatar_data_pt(datetime.now())} - Depósito: R$ {self.valor:.2f}"
            )
            print("\n Depósito realizado com sucesso! ")
            return True
        print("\n Operação falhou! Valor inválido. ")
        return False

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if self.valor > conta.saldo:
            print("\n Operação falhou! Saldo insuficiente. ")
            return False
        if self.valor > conta.limite:
            print("\n Operação falhou! Valor excede o limite. ")
            return False
        if conta.limite_saques <= 0:
            print("\n Operação falhou! Limite de saques atingido. ")
            return False
        if self.valor > 0:
            conta.saldo -= self.valor
            conta.limite_saques -= 1
            conta.historico.adicionar_transacao(
                f"{formatar_data_pt(datetime.now())} - Saque: R$ {self.valor:.2f}"
            )
            print("\n Saque realizado com sucesso! ")
            return True
        print("\n Operação falhou! Valor inválido. ")
        return False

class Conta(ABC):
    def __init__(self, numero, cliente):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = "0001"
        self.cliente = cliente
        self.historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return ContaCorrente(numero, cliente)

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500.0, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

class Cliente(ABC):
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        return transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

#SISTEMA 

clientes = []
contas = []

def buscar_cliente_por_cpf(cpf):
    for cliente in clientes:
        if isinstance(cliente, PessoaFisica) and cliente.cpf == cpf:
            return cliente
    return None

def criar_cliente():
    cpf = input("CPF (somente números): ").strip()
    if buscar_cliente_por_cpf(cpf):
        print("\n Já existe cliente com esse CPF! ")
        return
    nome = input("Nome completo: ").strip()
    data_nascimento = input("Data de nascimento (dd/mm/aaaa): ").strip()
    try:
        data_nasc = datetime.strptime(data_nascimento, "%d/%m/%Y").date()
    except ValueError:
        print("\n Data de nascimento inválida! ")
        return
    endereco = input("Endereço (logradouro, nro - bairro - cidade/sigla estado): ").strip()
    cliente = PessoaFisica(cpf, nome, data_nasc, endereco)
    clientes.append(cliente)
    print("\n Cliente criado com sucesso! ")

def criar_conta(cliente=None):
    if not cliente:
        cpf = input("Informe o CPF do cliente: ").strip()
        cliente = buscar_cliente_por_cpf(cpf)
        if not cliente:
            print("\n Cliente não encontrado! ")
            return
    numero = len(contas) + 1
    conta = Conta.nova_conta(cliente, numero)
    cliente.adicionar_conta(conta)
    contas.append(conta)
    print("\n Conta criada com sucesso! ")
    print(f"Agência: {conta.agencia} | Número da conta: {conta.numero}")

def listar_contas(cliente=None):
    lista = cliente.contas if cliente else contas
    if not lista:
        print("\n Nenhuma conta cadastrada. ")
        return
    for conta in lista:
        print("="*40)
        print(f"Agência: {conta.agencia}")
        print(f"Número da conta: {conta.numero}")
        print(f"Titular: {conta.cliente.nome}")
        print(f"CPF: {conta.cliente.cpf}")

def alterar_senha(cliente):
    print("\nFuncionalidade de alteração de senha não implementada.")

def acessar_conta():
    cpf = input("Informe o CPF do titular: ").strip()
    cliente = buscar_cliente_por_cpf(cpf)
    if not cliente or not cliente.contas:
        print("\n Cliente não encontrado ou sem contas. ")
        return
    print("\nContas do cliente:")
    for idx, conta in enumerate(cliente.contas, 1):
        print(f"[{idx}] Agência: {conta.agencia} | Conta: {conta.numero}")
    try:
        escolha = int(input("Escolha o número da conta: "))
        conta = cliente.contas[escolha-1]
    except (ValueError, IndexError):
        print("\n Opção inválida! ")
        return
    menu2(conta, cliente)

def menu1():
    while True:
        print("\n Bem-vindo ao Fesisbank! ")
        print("[1] Novo cliente")
        print("[2] Nova conta")
        print("[3] Listar contas")
        print("[4] Acessar conta")
        print("[5] Sair")
        opcao = input("=> ").strip()
        if opcao == "1":
            criar_cliente()
        elif opcao == "2":
            criar_conta()
        elif opcao == "3":
            listar_contas()
        elif opcao == "4":
            acessar_conta()
        elif opcao == "5":
            print("Obrigado por usar o Fesisbank!")
            break
        else:
            print("\n Opção inválida! ")

def menu2(conta, cliente):
    while True:
        print(f"\n Conta {conta.numero} | Saldo: R$ {conta.saldo:.2f} ")
        print("[1] Depositar")
        print("[2] Sacar")
        print("[3] Extrato")
        print("[4] Voltar")
        print("[5] Mais")
        opcao = input("=> ").strip()
        if opcao == "1":
            valor = float(input("Valor do depósito: "))
            transacao = Deposito(valor)
            cliente.realizar_transacao(conta, transacao)
        elif opcao == "2":
            valor = float(input("Valor do saque: "))
            transacao = Saque(valor)
            cliente.realizar_transacao(conta, transacao)
        elif opcao == "3":
            print("\n Extrato ")
            if not conta.historico.transacoes:
                print("Não foram realizadas movimentações.")
            else:
                for t in conta.historico.transacoes:
                    print(t)
            print(f"Saldo atual: R$ {conta.saldo:.2f}")
        elif opcao == "4":
            break
        elif opcao == "5":
            menu3(cliente)
        else:
            print("\n Opção inválida! ")

def menu3(cliente):
    while True:
        print("\n Mais opções ")
        print("[1] Criar nova conta")
        print("[2] Listar minhas contas")
        print("[3] Alterar minha senha")
        print("[4] Voltar")
        opcao = input("=> ").strip()
        if opcao == "1":
            criar_conta(cliente)
        elif opcao == "2":
            listar_contas(cliente)
        elif opcao == "3":
            alterar_senha(cliente)
        elif opcao == "4":
            break
        else:
            print("\n Opção inválida! ")

if __name__ == "__main__":
    menu1()
