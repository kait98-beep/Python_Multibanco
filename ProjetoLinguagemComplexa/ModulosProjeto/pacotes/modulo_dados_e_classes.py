from dataclasses import dataclass, field

UTILIZADOR_ATUAL = None

@dataclass
class UtilizadorConta:
    """Representa a conta de um utilizador do banco.

    Attributes:
        password (str): password do utilizador.
        saldo (float): saldo atual da conta.
        historico (list): lista de movimentos (depósitos e transferências).
    """

    password: str
    saldo: float = 0  # Inicialmente Zero
    historico: list = field(default_factory=list)
