"""
Bank Account Management System

This module implements a banking system with support for multiple account types,
clients, and transactions. It demonstrates OOP principles and clean architecture.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bank.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

DIAS_SEMANA_PT: List[str] = [
    "segunda-feira", "terça-feira", "quarta-feira",
    "quinta-feira", "sexta-feira", "sábado", "domingo"
]

def formatar_data_pt(dt: datetime) -> str:
    """
    Format a datetime object to Portuguese format with weekday.
    
    Args:
        dt: The datetime object to format
        
    Returns:
        A formatted string with weekday and date/time in PT-BR format
    """
    dia_semana = DIAS_SEMANA_PT[dt.weekday()]
    return f"{dia_semana.capitalize()}, {dt.strftime('%d/%m/%Y %H:%M')}"

#CLASSES UML

class Historico:
    """Class for managing transaction history."""
    
    def __init__(self) -> None:
        self.transacoes: List[str] = []

    def adicionar_transacao(self, transacao: str) -> None:
        """Add a new transaction to the history.
        
        Args:
            transacao: The transaction description to add
        """
        self.transacoes.append(transacao)
        logging.info(f"Nova transação registrada: {transacao}")

class Transacao(ABC):
    """Abstract base class for all transaction types."""
    
    @abstractmethod
    def registrar(self, conta: 'Conta') -> bool:
        """Register a transaction on an account.
        
        Args:
            conta: The account to perform the transaction on
            
        Returns:
            bool: True if transaction was successful, False otherwise
        """
        pass

class Deposito(Transacao):
    """Class representing a deposit transaction."""
    
    def __init__(self, valor: float) -> None:
        """
        Initialize a new deposit transaction.
        
        Args:
            valor: The amount to deposit
        """
        self.valor = valor

    def registrar(self, conta: 'Conta') -> bool:
        """
        Register a deposit transaction on an account.
        
        Args:
            conta: The account to deposit into
            
        Returns:
            bool: True if deposit was successful, False otherwise
        """
        if self.valor > 0:
            conta.saldo += self.valor
            transacao = f"{formatar_data_pt(datetime.now())} - Depósito: R$ {self.valor:.2f}"
            conta.historico.adicionar_transacao(transacao)
            logging.info(f"Depósito realizado com sucesso na conta {conta.numero}")
            print("\n Depósito realizado com sucesso! ")
            return True
        logging.warning(f"Tentativa de depósito com valor inválido: {self.valor}")
        print("\n Operação falhou! Valor inválido. ")
        return False

class Saque(Transacao):
    """Class representing a withdrawal transaction."""
    
    def __init__(self, valor: float) -> None:
        """
        Initialize a new withdrawal transaction.
        
        Args:
            valor: The amount to withdraw
        """
        self.valor = valor

    def registrar(self, conta: 'ContaCorrente') -> bool:
        """
        Register a withdrawal transaction on an account.
        
        Args:
            conta: The account to withdraw from
            
        Returns:
            bool: True if withdrawal was successful, False otherwise
        """
        if self.valor <= 0:
            logging.warning(f"Tentativa de saque com valor inválido: {self.valor}")
            print("\n Operação falhou! Valor inválido. ")
            return False
            
        if self.valor > conta.saldo:
            logging.warning(f"Tentativa de saque com saldo insuficiente na conta {conta.numero}")
            print("\n Operação falhou! Saldo insuficiente. ")
            return False
            
        if self.valor > conta.limite:
            logging.warning(f"Tentativa de saque acima do limite na conta {conta.numero}")
            print("\n Operação falhou! Valor excede o limite. ")
            return False
            
        if conta.limite_saques <= 0:
            logging.warning(f"Tentativa de saque com limite diário atingido na conta {conta.numero}")
            print("\n Operação falhou! Limite de saques atingido. ")
            return False
            
        conta.saldo -= self.valor
        conta.limite_saques -= 1
        transacao = f"{formatar_data_pt(datetime.now())} - Saque: R$ {self.valor:.2f}"
        conta.historico.adicionar_transacao(transacao)
        logging.info(f"Saque realizado com sucesso na conta {conta.numero}")
        print("\n Saque realizado com sucesso! ")
        return True

class Conta(ABC):
    """Abstract base class for all account types."""
    
    def __init__(self, numero: int, cliente: 'Cliente') -> None:
        """
        Initialize a new bank account.
        
        Args:
            numero: Account number
            cliente: Account holder
        """
        self.saldo: float = 0.0
        self.numero: int = numero
        self.agencia: str = "0001"
        self.cliente: 'Cliente' = cliente
        self.historico: Historico = Historico()
        self.limite: float = 0.0
        self.limite_saques: int = 0

    @classmethod
    def nova_conta(cls, cliente: 'Cliente', numero: int) -> 'ContaCorrente':
        """
        Factory method to create a new account.
        
        Args:
            cliente: Account holder
            numero: Account number
            
        Returns:
            A new ContaCorrente instance
        """
        return ContaCorrente(numero, cliente)

class ContaCorrente(Conta):
    """Class representing a checking account."""
    
    def __init__(self, numero: int, cliente: 'Cliente', limite: float = 500.0, limite_saques: int = 3) -> None:
        """
        Initialize a new checking account.
        
        Args:
            numero: Account number
            cliente: Account holder
            limite: Maximum withdrawal limit
            limite_saques: Daily withdrawal limit
        """
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        logging.info(f"Nova conta corrente criada: {numero} para cliente {cliente.nome}")

class Cliente(ABC):
    """Abstract base class for all client types."""

    def __init__(self, endereco: str) -> None:
        """
        Initialize a new client.
        
        Args:
            endereco: Client's address
        """
        self.endereco: str = endereco
        self.contas: List[Conta] = []
        self.nome: str = ""  # Will be set by child classes

    def realizar_transacao(self, conta: Conta, transacao: Transacao) -> bool:
        """
        Perform a transaction on an account.
        
        Args:
            conta: The account to perform the transaction on
            transacao: The transaction to perform
            
        Returns:
            bool: True if transaction was successful, False otherwise
        """
        return transacao.registrar(conta)

    def adicionar_conta(self, conta: Conta) -> None:
        """
        Add an account to this client.
        
        Args:
            conta: The account to add
        """
        self.contas.append(conta)
        logging.info(f"Nova conta {conta.numero} adicionada ao cliente {self.nome}")

class PessoaFisica(Cliente):
    """Class representing an individual client."""
    
    def __init__(self, cpf: str, nome: str, data_nascimento: datetime, endereco: str) -> None:
        """
        Initialize a new individual client.
        
        Args:
            cpf: Client's tax ID
            nome: Client's name
            data_nascimento: Client's birth date
            endereco: Client's address
        """
        super().__init__(endereco)
        self.cpf: str = cpf
        self.nome: str = nome
        self.data_nascimento: datetime = data_nascimento
        logging.info(f"Novo cliente PF criado: {nome} (CPF: {cpf})")

#SISTEMA 

clientes = []
contas = []

def buscar_cliente_por_cpf(cpf):
    for cliente in clientes:
        if isinstance(cliente, PessoaFisica) and cliente.cpf == cpf:
            return cliente
    return None

def criar_cliente() -> Optional[PessoaFisica]:
    """
    Create a new individual client with input validation.
    
    Returns:
        Optional[PessoaFisica]: The created client or None if creation failed
    """
    try:
        # Validate CPF
        cpf = input("CPF (somente números): ").strip()
        if not cpf.isdigit() or len(cpf) != 11:
            logging.warning(f"Tentativa de criação de cliente com CPF inválido: {cpf}")
            print("\n CPF inválido! Digite apenas números (11 dígitos).")
            return None
            
        if buscar_cliente_por_cpf(cpf):
            logging.warning(f"Tentativa de criação de cliente com CPF duplicado: {cpf}")
            print("\n Já existe cliente com esse CPF!")
            return None
            
        # Validate name
        nome = input("Nome completo: ").strip()
        if len(nome) < 3:
            logging.warning("Tentativa de criação de cliente com nome muito curto")
            print("\n Nome deve ter pelo menos 3 caracteres!")
            return None
            
        # Validate birth date
        data_nascimento = input("Data de nascimento (dd/mm/aaaa): ").strip()
        try:
            data_nasc = datetime.strptime(data_nascimento + " 00:00:00", "%d/%m/%Y %H:%M:%S")
        except ValueError:
            logging.warning(f"Tentativa de criação de cliente com data inválida: {data_nascimento}")
            print("\n Data de nascimento inválida!")
            return None
            
        # Validate address
        endereco = input("Endereço (logradouro, nro - bairro - cidade/sigla estado): ").strip()
        if len(endereco) < 10:
            logging.warning("Tentativa de criação de cliente com endereço muito curto")
            print("\n Endereço muito curto!")
            return None
            
        # Create client
        cliente = PessoaFisica(cpf, nome, data_nasc, endereco)
        clientes.append(cliente)
        logging.info(f"Cliente criado com sucesso: {nome} (CPF: {cpf})")
        print("\n Cliente criado com sucesso!")
        return cliente
        
    except Exception as e:
        logging.error(f"Erro ao criar cliente: {str(e)}")
        print("\n Ocorreu um erro ao criar o cliente. Tente novamente.")

def criar_conta(cliente: Optional[PessoaFisica] = None) -> Optional[Conta]:
    """
    Create a new account for a client with input validation.
    
    Args:
        cliente: Optional client to create account for. If None, will prompt for CPF.
        
    Returns:
        Optional[Conta]: The created account or None if creation failed
    """
    try:
        # Get client if not provided
        if not cliente:
            cpf = input("Informe o CPF do cliente: ").strip()
            if not cpf.isdigit() or len(cpf) != 11:
                logging.warning(f"Tentativa de criação de conta com CPF inválido: {cpf}")
                print("\nCPF inválido! Digite apenas números (11 dígitos).")
                return None
                
            cliente = buscar_cliente_por_cpf(cpf)
            if not cliente:
                logging.warning(f"Tentativa de criação de conta para cliente inexistente: {cpf}")
                print("\nCliente não encontrado!")
                return None
                
        # Create unique account number
        numero = len(contas) + 1
        
        # Create account
        conta = Conta.nova_conta(cliente, numero)
        cliente.adicionar_conta(conta)
        contas.append(conta)
        
        logging.info(f"Conta {numero} criada com sucesso para cliente {cliente.nome}")
        print("\nConta criada com sucesso!")
        print(f"Agência: {conta.agencia} | Número da conta: {conta.numero}")
        
        return conta
        
    except Exception as e:
        logging.error(f"Erro ao criar conta: {str(e)}")
        print("\nOcorreu um erro ao criar a conta. Tente novamente.")
        return None

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

def acessar_conta() -> None:
    """
    Access a client's account with input validation and error handling.
    """
    try:
        # Validate CPF
        cpf = input("Informe o CPF do titular: ").strip()
        if not cpf.isdigit() or len(cpf) != 11:
            logging.warning(f"Tentativa de acesso com CPF inválido: {cpf}")
            print("\nCPF inválido! Digite apenas números (11 dígitos).")
            return
            
        # Get client
        cliente = buscar_cliente_por_cpf(cpf)
        if not cliente:
            logging.warning(f"Tentativa de acesso com CPF inexistente: {cpf}")
            print("\nCliente não encontrado!")
            return
            
        # Check if client has accounts
        if not cliente.contas:
            logging.warning(f"Tentativa de acesso a cliente sem contas: {cpf}")
            print("\nCliente não possui contas cadastradas!")
            return
            
        # Display accounts
        print("\n=== Contas do Cliente ===")
        print(f"Cliente: {cliente.nome}")
        print(f"CPF: {cliente.cpf}")
        print("------------------------")
        for idx, conta in enumerate(cliente.contas, 1):
            print(f"[{idx}] Agência: {conta.agencia} | Conta: {conta.numero}")
        print("------------------------")
        
        # Get account choice
        try:
            escolha = int(input("Escolha o número da conta: "))
            if escolha < 1 or escolha > len(cliente.contas):
                logging.warning(f"Tentativa de acesso com número de conta inválido: {escolha}")
                print("\nNúmero de conta inválido!")
                return
                
            conta = cliente.contas[escolha-1]
            logging.info(f"Acesso bem-sucedido à conta {conta.numero} do cliente {cliente.nome}")
            menu2(conta, cliente)
            
        except ValueError:
            logging.warning("Tentativa de acesso com entrada não numérica")
            print("\nPor favor, digite apenas números!")
            return
            
    except Exception as e:
        logging.error(f"Erro ao acessar conta: {str(e)}")
        print("\nOcorreu um erro ao acessar a conta. Tente novamente.")

def exibir_menu_principal() -> str:
    """
    Display the main menu and get user input.
    
    Returns:
        str: The user's menu choice
    """
    print("\n=================================")
    print("     Bem-vindo ao Fesisbank!     ")
    print("=================================")
    print("[1] Novo cliente")
    print("[2] Nova conta")
    print("[3] Listar contas")
    print("[4] Acessar conta")
    print("[5] Sair")
    print("=================================")
    return input("=> ").strip()

def menu1() -> None:
    """Main application loop."""
    
    logging.info("Iniciando aplicação Fesisbank")
    
    while True:
        try:
            opcao = exibir_menu_principal()
            
            if opcao == "1":
                criar_cliente()
                
            elif opcao == "2":
                criar_conta()
                
            elif opcao == "3":
                listar_contas()
                
            elif opcao == "4":
                acessar_conta()
                
            elif opcao == "5":
                print("\nObrigado por usar o Fesisbank!")
                logging.info("Encerrando aplicação Fesisbank")
                break
                
            else:
                print("\nOpção inválida! Por favor, escolha uma opção de 1 a 5.")
                logging.warning(f"Tentativa de acesso com opção inválida: {opcao}")
                
        except Exception as e:
            logging.error(f"Erro no menu principal: {str(e)}")
            print("\nOcorreu um erro inesperado. Por favor, tente novamente.")

def exibir_menu_conta(conta: Conta) -> str:
    """
    Display the account operations menu.
    
    Args:
        conta: The current account
        
    Returns:
        str: The user's menu choice
    """
    print("\n=================================")
    print(f"     Conta: {conta.numero}        ")
    print(f"     Saldo: R$ {conta.saldo:.2f}     ")
    print("=================================")
    print("[1] Depositar")
    print("[2] Sacar")
    print("[3] Extrato")
    print("[4] Voltar")
    print("[5] Mais opções")
    print("=================================")
    return input("=> ").strip()

def processar_deposito(conta: Conta, cliente: Cliente) -> None:
    """Process a deposit transaction with input validation."""
    valor_str = input("Valor do depósito: R$ ").strip()
    try:
        valor = float(valor_str)
        transacao = Deposito(valor)
        cliente.realizar_transacao(conta, transacao)
    except ValueError:
        logging.warning(f"Tentativa de depósito com valor inválido: {valor_str}")
        print("\nValor inválido! Digite apenas números.")

def processar_saque(conta: Conta, cliente: Cliente) -> None:
    """Process a withdrawal transaction with input validation."""
    valor_str = input("Valor do saque: R$ ").strip()
    try:
        valor = float(valor_str)
        transacao = Saque(valor)
        cliente.realizar_transacao(conta, transacao)
    except ValueError:
        logging.warning(f"Tentativa de saque com valor inválido: {valor_str}")
        print("\nValor inválido! Digite apenas números.")

def exibir_extrato(conta: Conta) -> None:
    """Display account statement."""
    print("\n======= EXTRATO =======")
    if not conta.historico.transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in conta.historico.transacoes:
            print(transacao)
    print("----------------------")
    print(f"Saldo atual: R$ {conta.saldo:.2f}")
    print("======================")

def menu2(conta: Conta, cliente: PessoaFisica) -> None:
    """
    Account operations menu with input validation and error handling.
    
    Args:
        conta: The account to operate on
        cliente: The account owner
    """
    logging.info(f"Iniciando operações na conta {conta.numero} do cliente {cliente.nome}")
    
    while True:
        try:
            opcao = exibir_menu_conta(conta)
            
            if opcao == "1":
                processar_deposito(conta, cliente)
                
            elif opcao == "2":
                processar_saque(conta, cliente)
                
            elif opcao == "3":
                exibir_extrato(conta)
                
            elif opcao == "4":
                logging.info(f"Encerrando operações na conta {conta.numero}")
                break
                
            elif opcao == "5":
                menu3(cliente)
                
            else:
                print("\nOpção inválida! Por favor, escolha uma opção de 1 a 5.")
                logging.warning(f"Tentativa de operação com opção inválida: {opcao}")
                
        except Exception as e:
            logging.error(f"Erro no menu de conta: {str(e)}")
            print("\nOcorreu um erro inesperado. Por favor, tente novamente.")

def exibir_menu_adicional() -> str:
    """
    Display additional options menu.
    
    Returns:
        str: The user's menu choice
    """
    print("\n=================================")
    print("         Mais Opções             ")
    print("=================================")
    print("[1] Criar nova conta")
    print("[2] Listar minhas contas")
    print("[3] Alterar minha senha")
    print("[4] Voltar")
    print("=================================")
    return input("=> ").strip()

def menu3(cliente: PessoaFisica) -> None:
    """
    Additional options menu with input validation and error handling.
    
    Args:
        cliente: The current client
    """
    logging.info(f"Acessando menu adicional para cliente {cliente.nome}")
    
    while True:
        try:
            opcao = exibir_menu_adicional()
            
            if opcao == "1":
                criar_conta(cliente)
                
            elif opcao == "2":
                listar_contas(cliente)
                
            elif opcao == "3":
                logging.info("Tentativa de alteração de senha - funcionalidade não implementada")
                print("\nFuncionalidade de alteração de senha será implementada em breve!")
                
            elif opcao == "4":
                logging.info(f"Saindo do menu adicional para cliente {cliente.nome}")
                break
                
            else:
                print("\nOpção inválida! Por favor, escolha uma opção de 1 a 4.")
                logging.warning(f"Tentativa de acesso com opção inválida no menu adicional: {opcao}")
                
        except Exception as e:
            logging.error(f"Erro no menu adicional: {str(e)}")
            print("\nOcorreu um erro inesperado. Por favor, tente novamente.")

if __name__ == "__main__":
    menu1()
