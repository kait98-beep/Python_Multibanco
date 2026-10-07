class UtilizadorJaExisteError(Exception):
    """Levantada quando se cria um utilizador com um username que já existe."""

class UtilizadorInexistenteError(Exception):
    """Levantada quando se transfere para um username que não existe."""

class SaldoInsuficienteError(Exception):
    """Levantada quando se transfere um valor superior ao saldo da conta."""

class ProprioUtilizadorError(Exception):
    """Levantada quando se tenta transferir dinheiro para a própria conta."""
