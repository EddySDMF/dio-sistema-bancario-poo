from classes_poo import *
from datetime import datetime

def menu():
    menu = """
===================== SISTEMA BANCARIO =====================
    [d]  Depositar
    [s]  Sacar
    [e]  Extrato
    [nc] Nova conta
    [lc] Listar contas
    [nu] Novo usuario
    [lu] Listar usuarios
    [q]  Sair
    => """
    return input(menu)

def depositar(clientes, contas):
    cpf = input("Informe o CPF (somente numeros): ")

    if cpf.isdigit():
        cliente = filtrar_clientes(cpf, clientes)
        if not cliente:
            print("Cliente nao encontrado!")
            return
        
        numero_conta = input("Informe o numero da conta: ")

        if numero_conta.isdigit():
            numero_conta = float(numero_conta)
            conta = filtrar_contas(numero_conta, contas, cliente)
            if not conta:
                print("Conta nao encontrada!")
                return

            valor = float(input("Quanto deseja depositar? "))
            transacao = Deposito(valor)

            # cliente.realizar_transacao(conta, transacao)
            transacao.registrar(conta)
        else:
            print("Numero de conta invalido!")
    else:
        print("Numero de CPF invalido!")

def sacar(clientes, contas):
    cpf = input("Informe o CPF (somente numeros): ")

    if cpf.isdigit():
        cliente = filtrar_clientes(cpf, clientes)
        if not cliente:
            print("Cliente nao encontrado!")
            return
        
        numero_conta = input("Informe o numero da conta: ")

        if numero_conta.isdigit():
            numero_conta = float(numero_conta)
            conta = filtrar_contas(numero_conta, contas, cliente)
            if not conta:
                print("Conta nao encontrada!")
                return

            valor = float(input("Quanto deseja sacar? "))
            transacao = Saque(valor)

            # cliente.realizar_transacao(conta, transacao)
            transacao.registrar(conta)
        else:
            print("O numero da conta é invalido!")
    else:
        print("O numero do CPF é invalido!")

def extrato_completo(clientes, contas):
    cpf = input("Informe o CPF (somente numeros): ")

    if cpf.isdigit():
        cliente = filtrar_clientes(cpf, clientes)
        if not cliente:
            print("Cliente nao encontrado!")
            return
        
        numero_conta = input("Informe o numero da conta: ")

        if numero_conta.isdigit():
            numero_conta = float(numero_conta)
            conta = filtrar_contas(numero_conta, contas, cliente)
            if not conta:
                print("Conta nao encontrada!")
                return
            
            print("\n======================= EXTRATO =======================")
            transacoes = conta.historico.transacoes
            saques_realizados = len(
                [transacao for transacao in transacoes if transacao["tipo"] == Saque.__name__]
            )
            qtd_saques = conta.limite_saques - saques_realizados

            if not transacoes:
                print("Nao houveram movimentaçoes nesta conta.")
            else:
                for transacao in transacoes:
                    print(f"Tipo: {transacao['tipo']} | Valor: {transacao['valor']} | Data: {transacao['data']}")
            print(f"Saques Restantes: {qtd_saques}")
            print(f"Saldo: {conta.saldo:.2f}")
            
        else:
            print("Numero de conta invalido!")
    else:
        print("Numero de CPF invalido!")

def gravar_transacao(quantia, extrato):
    data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if opcao == "d":
        extrato.append([data, "Deposito", quantia])
    elif opcao == "s":
        extrato.append([data, "Saque", quantia])

def criar_cliente(clientes):
    cpf = input("Digite o CPF (somente números): ")
    cliente = filtrar_clientes(cpf, clientes)

    if cliente:
        print("Usuário já existe!")
        return False

    nome = input("Nome: ")
    data_nascimento = input("Data de nascimento: ")
    endereco = input("Endereço: (logradouro, nro - bairro - cidade/sigla estado) ")

    cliente = PessoaFisica(
        endereco = endereco, 
        cpf = cpf, 
        nome = nome, 
        data_nascimento = data_nascimento
    )
    clientes.append(cliente)

    print("Cliente criado com sucesso!")

def filtrar_clientes(cpf, clientes):
    cliente_filtrado = [cliente for cliente in clientes if cliente.cpf == cpf]
    return cliente_filtrado[0] if cliente_filtrado else None

def criar_conta_corrente(numero_conta, clientes, contas):
    cpf = input("Digite o CPF (somente números): ")
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print("Usuário não encontrado!")
        return False

    conta = ContaCorrente.nova_conta(
        numero_conta = numero_conta,
        cliente = cliente
    )
    # cliente.contas.append(conta)
    contas.append(conta)
    
    print("Conta criada com sucesso!")

def filtrar_contas(numero_conta, contas, cliente):
    conta_filtrada = [conta for conta in contas if conta.cliente == cliente and conta.numero_conta == numero_conta]
    return conta_filtrada[0] if conta_filtrada else None

def listar_contas(contas):
    print("==================== CONTAS =========================")

    for conta in contas:
        print(f"Conta: {conta.numero_conta} | Cliente: {conta.cliente.nome} | Agencia: {conta.agencia} | Saldo: {conta.saldo}")

def listar_clientes(clientes):
    print("=================== CLIENTES ========================")

    for cliente in clientes:
        print(f"Titular: {cliente.nome} | CPF: {cliente.cpf} | Nascimento: {cliente.data_nascimento} | Endereço: {cliente.endereco}")
     
def main():

    clientes = []
    contas = []

    while True:
        
        opcao = menu()

        if opcao == "d":
            depositar(clientes, contas)
 
        elif opcao == "s":
            sacar(clientes, contas)

        elif opcao == "e":
            extrato_completo(clientes, contas)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta_corrente(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "nu":
            criar_cliente(clientes)
        
        elif opcao == "lu":
            listar_clientes(clientes)

        elif opcao == "q":
            break

        else:
            print('Operaçao invalida!')

main()