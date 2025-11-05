"""
Web interface for the Bank Account Management System using Streamlit
"""

import streamlit as st
import pickle
from datetime import datetime
from pathlib import Path
from bank_account import (
    PessoaFisica, Conta, Deposito, Saque,
    buscar_cliente_por_cpf
)

# Initialize persistent storage
def load_data():
    """Load data from pickle file or initialize if not exists"""
    data_file = Path("bank_data.pkl")
    if data_file.exists():
        with open(data_file, "rb") as f:
            data = pickle.load(f)
            return data["clientes"], data["contas"]
    return [], []

def save_data(clientes, contas):
    """Save data to pickle file"""
    with open("bank_data.pkl", "wb") as f:
        pickle.dump({"clientes": clientes, "contas": contas}, f)

# Initialize global variables
if "clientes" not in st.session_state:
    st.session_state.clientes, st.session_state.contas = load_data()

clientes = st.session_state.clientes
contas = st.session_state.contas

def init_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'current_client' not in st.session_state:
        st.session_state.current_client = None
    if 'current_account' not in st.session_state:
        st.session_state.current_account = None

def login_page():
    """Display login page"""
    st.title("🏦 FesisBank - Login")
    
    with st.form("login_form"):
        cpf = st.text_input("CPF (somente números):")
        submitted = st.form_submit_button("Entrar")
        
        if submitted:
            if cpf.isdigit() and len(cpf) == 11:
                cliente = buscar_cliente_por_cpf(cpf)
                if cliente:
                    st.session_state.authenticated = True
                    st.session_state.current_client = cliente
                    st.success("Login realizado com sucesso!")
                    st.rerun()
                else:
                    st.error("Cliente não encontrado!")
            else:
                st.error("CPF inválido!")

def create_account_page():
    """Display account creation page"""
    st.title("📝 Criar Nova Conta")
    
    with st.form("create_account_form"):
        cpf = st.text_input("CPF (somente números):")
        nome = st.text_input("Nome completo:")
        data_nascimento = st.date_input("Data de nascimento:")
        endereco = st.text_input("Endereço completo:")
        submitted = st.form_submit_button("Criar Conta")
        
        if submitted:
            if not cpf.isdigit() or len(cpf) != 11:
                st.error("CPF inválido!")
                return
                
            if buscar_cliente_por_cpf(cpf):
                st.error("CPF já cadastrado!")
                return
                
            if len(nome) < 3:
                st.error("Nome muito curto!")
                return
                
            if len(endereco) < 10:
                st.error("Endereço muito curto!")
                return
                
            # Create new client
            data_nasc = datetime.combine(data_nascimento, datetime.min.time())
            cliente = PessoaFisica(cpf, nome, data_nasc, endereco)
            clientes.append(cliente)
            
            # Create account
            numero = len(contas) + 1
            conta = Conta.nova_conta(cliente, numero)
            cliente.adicionar_conta(conta)
            contas.append(conta)
            save_data(clientes, contas)
            
            st.success("Conta criada com sucesso!")
            st.write(f"Agência: {conta.agencia} | Conta: {conta.numero}")

def account_operations():
    """Display account operations page"""
    client = st.session_state.current_client
    st.title(f"👤 Bem-vindo(a), {client.nome}!")
    
    if not client.contas:
        st.warning("Você não possui contas cadastradas.")
        return
        
    # Account selection
    account_options = {f"Conta {c.numero}": c for c in client.contas}
    selected_account = st.selectbox(
        "Selecione uma conta:",
        options=list(account_options.keys())
    )
    
    conta = account_options[selected_account]
    st.session_state.current_account = conta
    
    # Display balance
    st.header(f"💰 Saldo: R$ {conta.saldo:.2f}")
    
    # Operations
    col1, col2 = st.columns(2)
    
    with col1:
        with st.form("deposit_form"):
            st.subheader("📥 Depósito")
            valor_dep = st.number_input("Valor:", min_value=0.01, step=0.01, key="dep")
            if st.form_submit_button("Depositar"):
                transacao = Deposito(valor_dep)
                if client.realizar_transacao(conta, transacao):
                    st.success("Depósito realizado com sucesso!")
                    st.rerun()
    
    with col2:
        with st.form("withdraw_form"):
            st.subheader("📤 Saque")
            valor_saq = st.number_input("Valor:", min_value=0.01, step=0.01, key="saq")
            if st.form_submit_button("Sacar"):
                transacao = Saque(valor_saq)
                if client.realizar_transacao(conta, transacao):
                    st.success("Saque realizado com sucesso!")
                    st.rerun()
    
    # Transaction history
    st.header("📋 Extrato")
    if conta.historico.transacoes:
        for transacao in conta.historico.transacoes:
            st.text(transacao)
    else:
        st.info("Não há transações registradas.")

def main():
    """Main application"""
    st.set_page_config(
        page_title="FesisBank Web",
        page_icon="🏦",
        layout="wide"
    )
    
    init_session_state()
    
    # Sidebar
    with st.sidebar:
        st.title("🏦 FesisBank")
        if st.session_state.authenticated:
            if st.button("Sair"):
                st.session_state.authenticated = False
                st.session_state.current_client = None
                st.session_state.current_account = None
                st.rerun()
        else:
            st.write("Faça login ou crie uma conta")
    
    # Main content
    if not st.session_state.authenticated:
        tab1, tab2 = st.tabs(["Login", "Criar Conta"])
        with tab1:
            login_page()
        with tab2:
            create_account_page()
    else:
        account_operations()

if __name__ == "__main__":
    main()