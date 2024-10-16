from abc import ABC, abstractmethod
from datetime import datetime

class Transacao(ABC):
    @property
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        self.conta = conta

class Deposito(Transacao):
    def __init__(self, valor):
        self.__valor = valor

    @property
    def valor(self):
        return self.__valor
    
    def registrar(self, conta):
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self.__valor = valor
    
    @property
    def valor(self):
        return self.__valor

    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)

class Cliente():
    def __init__(self, endereco: str):
        self.__endereco = endereco
        self.__contas = []
    
    @property
    def endereco(self):
        return self.__endereco

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        pass

class PessoaFisica(Cliente):
    def __init__(self, endereco: str, cpf: str, nome: str, data_nascimento):
        super().__init__(endereco)
        self.__cpf = cpf
        self.__nome = nome
        self.__data_nascimento = data_nascimento
    
    @property
    def cpf(self):
        return self.__cpf
    
    @property
    def nome(self):
        return self.__nome
    
    @property
    def data_nascimento(self):
        return self.__data_nascimento
    
    def __str__(self):
        return (f"""
            nome: {self.nome}
            cpf: {self.cpf}
            data_nascimento: {self.data_nascimento}
            endereco: {self.endereco}
        """)

class Historico():
    def __init__(self) -> None:
        self.__transacoes = []
    
    @property
    def transacoes(self):
        return self.__transacoes

    def adicionar_transacao(self, transacao):
        self.__transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }
        )

class Conta():
    def __init__(self, numero_conta, cliente):
        self.__saldo = 0
        self.__numero_conta = numero_conta
        self.__agencia = "0001"
        self.__cliente = cliente
        self.__historico = Historico()

    @property
    def saldo(self):
        return self.__saldo
    
    @property
    def numero_conta(self):
        return self.__numero_conta
    
    @property
    def agencia(self):
        return self.__agencia
    
    @property
    def cliente(self):
        return self.__cliente
    
    @property
    def historico(self):
        return self.__historico
    
    @classmethod
    def nova_conta(cls, cliente, numero_conta):
        return cls(numero_conta, cliente)
    
    def sacar(self, valor):
        # saldo = self.saldo
        # excedeu_saldo = valor > saldo
        
        if valor > 0:
            self.__saldo -= valor
            print(f"Saque de R${valor:.2f} realizado com sucesso!")
            return True
        
            # if excedeu_saldo:
            #     print("Voce nao possui saldo suficiente!")
            # else:
            #     self.__saldo -= valor
            #     print(f"Saque de R${valor:.2f} realizado com sucesso!")
            #     return True

        else:
            print("O valor para o saque é invalido!")
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self.__saldo += valor
            print(f"Deposito de R${valor:.2f} realizado com sucesso!")
        else:
            print("O valor para o deposito é invalido!")
            return False
        return True

class ContaCorrente(Conta):
    def __init__(self, numero_conta: int,  cliente: str, limite=500, limite_saques=3):
        super().__init__(numero_conta, cliente)
        self.__limite = limite
        self.__limite_saques = limite_saques
    
    @property
    def limite_saques(self):
        return self.__limite_saques

    def sacar(self, valor):
        qtd_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )
        excedeu_limite = valor > self.__limite
        excedeu_saques = qtd_saques >= self.__limite_saques
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_limite:
            print("O valor de saque excede o limite!")
        elif excedeu_saques:
            print("Numero maximo de saques excedido!")
        elif excedeu_saldo:
            print("Saldo insuficiente!")
        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return (f"""
            numero_conta: {self.numero_conta}
            cliente: {self.cliente.nome}
            agencia: {self.agencia}
            saldo: {self.saldo}
            historico: {self.historico.transacoes}
        """)
