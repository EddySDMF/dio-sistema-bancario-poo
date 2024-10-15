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

def depositar(clientes):
    cpf = input("Digite o CPF (somente números): ")
    cliente = filtrar_usuarios(cpf, clientes)

    if not cliente:
        print("Usuario nao encontrado!")
        return False
    
    return True

def sacar(*, saldo, quantia, numero_saques, limite_por_saque, LIMITE_SAQUES):
    regra_saldo = saldo >= quantia
    regra_limite = limite_por_saque >= quantia
    regra_saque = numero_saques < LIMITE_SAQUES
    if quantia > 0:
        if not regra_saldo:
            print("Voce nao tem saldo para realizar esta operaçao. Confira no extrato e tente novamente.")
        elif not regra_limite:
            print("Voce nao tem limite para realizar esta operaçao. Confira no extrato e tente novamente.")
        elif not regra_saque:
            print("Voce nao tem saque disponivel para realizar esta operaçao. Confira no extrato e tente novamente.")
        else:
            saldo -= quantia
            numero_saques += 1
            print(f"Seu saque de R${quantia:.2f} foi efetuado!")

def extrato_completo(saldo, /, *, extrato, numero_saques, LIMITE_SAQUES):
    qtd_saques = LIMITE_SAQUES - numero_saques
    cabecalhos = ["Data", "Tipo", "Valor"]
    print("===================  EXTRATO ========================")
    print(f"Seu saldo é de R${saldo:.2f}.")
    print(f"Voce tem {qtd_saques} saque(s).")
    print("=================== HISTORICO =======================")
    if extrato:
        print(f"{cabecalhos[0].center(20)} | {cabecalhos[1].center(10)} | {cabecalhos[2].center(10)}")
        for reg in extrato:
            print(f"{reg[0].center(20)} | {reg[1].center(10)} | {reg[2]}")
    else:
        print("Nao houveram movimentaçoes.")

def gravar_transacao(quantia, extrato):
    data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if opcao == "d":
        extrato.append([data, "Deposito", quantia])
    elif opcao == "s":
        extrato.append([data, "Saque", quantia])

def filtrar_clientes(cpf, clientes):
    cliente_filtrado = [cliente for cliente in clientes if cliente.cpf == cpf]
    return cliente_filtrado[0] if cliente_filtrado else None

def filtrar_conta(cpf, contas):
    pass

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

    print("============= Cliente criado com sucesso! =============")

def criar_conta_corrente(numero_conta, clientes, contas):
    cpf = input("Digite o CPF (somente números): ")
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print("Usuário não encontrado!")
        return False

    conta = ContaCorrente.nova_conta(
        numero = numero_conta,
        cliente = cliente
    )
    contas.append(conta)
    # cliente.contas.append(conta)
    
    print("Conta criada com sucesso!")

def listar_contas(contas):
    print("=================== CONTAS ========================")

    for conta in contas:
        print(conta)

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
            depositar(clientes)
 
        # elif opcao == "s":
        #     quantia = float(input("Qual quantia deseja sacar? "))
        #     sacar(
        #         saldo = saldo, 
        #         quantia = quantia, 
        #         numero_saques = numero_saques, 
        #         limite_por_saque = limite_por_saque, 
        #         LIMITE_SAQUES = LIMITE_SAQUES
        #     )
        #     gravar_transacao(quantia, extrato)

        # elif opcao == "e":
        #     extrato_completo(
        #         saldo, extrato = extrato, 
        #         numero_saques = numero_saques, 
        #         LIMITE_SAQUES = LIMITE_SAQUES
        #     )

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