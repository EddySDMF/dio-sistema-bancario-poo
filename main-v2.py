"""
REGRAS DO SISTEMAS

"""

from datetime import datetime


def menu():
    menu = """
===================== SISTEMA BANCARIO =====================
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nc] Nova conta
    [lc] Listar contas
    [nu] Novo usuario
    [q] Sair
    => """
    return input(menu)


def depositar(saldo, quantia, /):
    if quantia > 0:
        saldo += quantia
        print(f"Seu deposito de R${quantia:.2f} foi efetuado!")
    else:
        print("Nao foi possivel realizar o deposito. Tente novamente.")


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


def filtrar_usuarios(cpf, usuarios):
    usuario_filtrado = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuario_filtrado[0] if usuario_filtrado else None


def criar_usuario(usuarios):

    cpf = input("Digite o CPF (somente números): ")
    usuario = filtrar_usuarios(cpf, usuarios)

    if usuario:
        print("Usuário já existe")
        return

    nome = input("Nome: ")
    data_nascimento = input("Data de nascimento: ")
    endereco = input("Endereço: (logradouro, nro - bairro - cidade/sigla estado) ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("=== Usuário criado com sucesso! ===")


def criar_conta_corrente(agencia, numero_conta, usuarios):

    cpf = input("Digite o CPF (somente números): ")
    usuario = filtrar_usuarios(cpf, usuarios)

    if usuario:
        print("=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    else:
        print("=== Usuário não encontrado! ===")


def listar_contas(contas):
    print("=================== CONTAS ========================")

    for conta in contas:
        saida = f"""
            Agencia: {conta['agencia']}
            Conta Corrente: {conta['numero_conta']}
            Titular: {conta['usuario']}
        """
        print(saida)
        

def main():

    LIMITE_SAQUES = 10
    AGENCIA = "0001"

    saldo = 0
    limite_por_saque = 500
    extrato = []
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        
        opcao = menu()

        if opcao == "d":
            quantia = float(input("Qual quantia deseja depositar? "))
            depositar(saldo, quantia)
            gravar_transacao(quantia, extrato)

        elif opcao == "s":
            quantia = float(input("Qual quantia deseja sacar? "))
            sacar(
                saldo = saldo, 
                quantia = quantia, 
                numero_saques = numero_saques, 
                limite_por_saque = limite_por_saque, 
                LIMITE_SAQUES = LIMITE_SAQUES
            )
            gravar_transacao(quantia, extrato)

        elif opcao == "e":
            extrato_completo(
                saldo, extrato = extrato, 
                numero_saques = numero_saques, 
                LIMITE_SAQUES = LIMITE_SAQUES
            )

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta_corrente(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)
    

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "q":
            break

        else:
            print('Operaçao invalida!')

if __name__ == "__main__":
    main()