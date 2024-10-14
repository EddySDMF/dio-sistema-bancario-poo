from abc import ABC, abstractmethod
from datetime import datetime

class Transacao(ABC):
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
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self.__valor = valor
    
    @property
    def valor(self):
        return self.__valor

    def registrar(self, conta):
        pass

class Cliente():
    def __init__(self, endereco: str):
        self.__endereco = endereco
        self.__contas = []
    
    @property
    def endereco(self):
        return self.__endereco

    def realizar_transacao(self, conta, transacao):
        pass

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

class Historico():
    def __init__(self) -> None:
        self.__transacoes = []

    def adicionar_transacao(self, transacao):
        pass

class Conta():
    def __init__(self, numero, cliente):
        self.__saldo = 0
        self.__numero = numero
        self.__agencia = "0001"
        self.__cliente = cliente
        self.__historico = Historico()

    @property
    def saldo(self):
        return self.__saldo
    
    @property
    def numero(self):
        return self.__numero
    
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
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    def depositar(self, valor: float) -> bool:
        if valor > 0:
            self.__saldo = valor
            print(f"Seu deposito de R${valor:.2f} foi efetuado!")
        else:
            print("Nao foi possivel realizar o deposito. Tente novamente.")
            return False
        return True

    def sacar(self, valor: float) -> bool:
        pass

class ContaCorrente(Conta):
    def __init__(self, numero: int,  cliente: str, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.__limite = limite
        self.__limite_saques = limite_saques
    
    def sacar(self, contas):
        pass

    def __str__(self):
        return (f"Agencia: {self.agencia} | C/C: {self.numero} | Titular: {self.cliente.nome}")
