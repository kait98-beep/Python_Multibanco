import datetime
from ModulosProjeto.pacotes import (
    modulo_dados_e_classes,
    modulos_file_manipulation,
    modulos_excecoes
)

def conta_atual():
    """Devolve a conta (UtilizadorConta) de quem está atualmente logado

    Returns:
        UtilizadorConta | None: conta lida do ficheiro, ou None se o utilizador
        atual não existir.
    """

    return carregar_utilizador_para_memoria(modulo_dados_e_classes.UTILIZADOR_ATUAL)

def carregar_utilizador_para_memoria(username):
    """Lê o utilizador do ficheiro e constrói um objeto UtilizadorConta

    Args:
        username (str): nome do utilizador a carregar.

    Returns:
        UtilizadorConta | None: conta do utilizador, ou None se não existir
        no ficheiro.
    """

    dados = modulos_file_manipulation.encontrar_utilizador(username)
    if dados is None:
        return None
    return modulo_dados_e_classes.UtilizadorConta(
        password=dados["Password"],
        saldo=dados["Saldo"],
        historico=dados["Historico"]
    )

def depositar():
    """Solicita um valor ao utilizador e atualiza esses dados
    """

    conta = conta_atual()
    valor_depositar = float(input("Qual o valor que quer depositar: "))

    if valor_depositar > 0:
        conta.saldo += valor_depositar
        conta.historico.append(f"Deposito de {valor_depositar}")
        modulos_file_manipulation.atualizar_utilizador(
            username=modulo_dados_e_classes.UTILIZADOR_ATUAL,
            saldo=conta.saldo,
            historico=conta.historico
        )
        print(f"Depositado {valor_depositar} na conta\n")
    else:
        print("Valor a depositar é inferior a zero!\n")
        return


def consultar_saldo():
    """Consultar saldo Atual
    """

    conta = conta_atual()
    return f"O valor do saldo é: {conta.saldo}\n"


def consultar_retorno(numero_meses, taxa_juro):
    """Consultar retorno com Taxa de Juro Composto e com recursividade

    Args:
        numero_meses (int): número de meses, entre 1 e 12.
        taxa_juro (float): taxa de juro mensal em percentagem, entre 0 e 100.

    Returns:
        float | None: saldo da conta com juro composto aplicado, ou None se a
        taxa ou o número de meses forem inválidos.
    """

    conta = conta_atual()
    if not (0 <= taxa_juro <= 100 and 1 <= numero_meses <= 12):
        print("Taxa de juro inserido inválido ou Numero de meses inválido")
        return

    if numero_meses == 1:
        return conta.saldo * (1 + (taxa_juro / 100)** numero_meses)
    else:
        return consultar_retorno(numero_meses - 1, taxa_juro) * (1 + taxa_juro / 100)

def transferencia():
    """Transferência de um valor entre dois utilizadores

    Raises:
        modulos_excecoes.SaldoInsuficienteError: se o valor a transferir for 
        inferior ao que o utilizador tem na conta
        
        modulos_excecoes.UtilizadorInexistenteError: se o nome do utilizador 
        inserido não existir em dados_guardados.json
        
        modulos_excecoes.ProprioUtilizador: se o utilizador tentar transferir
        para a sua própria conta.
    """

    conta_origem = conta_atual()
    destino_username = input("Qual é a conta a quem quer transferir o dinheiro: ")
    valor = float(input("Qual o valor que pretende transferir: "))

    if destino_username == modulo_dados_e_classes.UTILIZADOR_ATUAL:
        raise modulos_excecoes.ProprioUtilizadorError(
            "Não pode transferir para si próprio."
        )

    if valor <= 0:
        print("O valor a transferir tem de ser superior a zero.\n")
        return

    if conta_origem.saldo < valor:
        raise modulos_excecoes.SaldoInsuficienteError("Saldo insuficiente")

    if modulos_file_manipulation.encontrar_utilizador(destino_username) is not None:
        conta_destino = carregar_utilizador_para_memoria(destino_username)
        conta_origem.saldo -= valor
        conta_destino.saldo += valor
        data = datetime.datetime.now()

        conta_origem.historico.append(
            f"Transferencia: enviado para {destino_username} em {data}, o valor de {valor}"
        )
        conta_destino.historico.append(
            f"Transferencia: recebido de {modulo_dados_e_classes.UTILIZADOR_ATUAL} em {data}, o valor de {valor}"
        )

        modulos_file_manipulation.atualizar_utilizador(
            username=modulo_dados_e_classes.UTILIZADOR_ATUAL,
            saldo=conta_origem.saldo,
            historico=conta_origem.historico
        )
        modulos_file_manipulation.atualizar_utilizador(
            username=destino_username,
            saldo=conta_destino.saldo,
            historico=conta_destino.historico
        )

        print("Transferência concluída com sucesso.\n")
        print(f"Dados de transferência: {data}")
    else:
        raise modulos_excecoes.UtilizadorInexistenteError(
            "Opção inválida ou utilizador não existe."
        )
