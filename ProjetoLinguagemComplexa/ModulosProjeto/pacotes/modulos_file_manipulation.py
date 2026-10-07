import json
import os

FILE_PATH = "dados_guardados.json"

def guardar_dados(dados):
    """Guarda a lista de utilizadores no ficheiro JSON, substituindo o conteúdo anterior.

    Args:
        dados (list): lista de dicionários, um por utilizador.
    """

    with open(FILE_PATH, "w", encoding="utf-8") as ficheiro:
        json.dump(dados, ficheiro, indent = 4, default=str)

def carregar_dados():
    """Lê os utilizadores guardados no ficheiro JSON.

    Returns:
        list: lista de dicionários, um por utilizador. Devolve uma lista vazia
        se o ficheiro não existir ou estiver vazio.
    """

    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, "r", encoding="utf-8") as ficheiro:
        conteudo = ficheiro.read().strip()
        # Se depois de ler retornar ""
        if not conteudo:
            return []
        # Retorna se existir
        return json.loads(conteudo)

def adicionar_utilizador(username, password):
    """Adiciona um novo utilizador ao ficheiro JSON, com saldo 0 e histórico vazio.

    Args:
        username (str): nome do novo utilizador.
        password (str): password do novo utilizador.
    """

    dados = carregar_dados()
    # Constroi um dicionário para o novo utilizador
    novo_utilizador = {
        "Username": username,
        "Password": password,
        "Saldo": 0,
        "Historico": []
    }
    dados.append(novo_utilizador)
    guardar_dados(dados)

def encontrar_utilizador(username):
    """Procura um utilizador no ficheiro JSON pelo username.

    Args:
        username (str): nome do utilizador a procurar.

    Returns:
        dict | None: dicionário do utilizador (Username, Password, Saldo, Historico)
        ou None se não existir.
    """

    dados = carregar_dados()
    for utilizador in dados:
        if utilizador["Username"] == username:
            return utilizador
    return None

def atualizar_utilizador(username, saldo, historico):
    """Atualiza o saldo e o histórico de um utilizador, sem alterar os restantes.

    Args:
        username (str): nome do utilizador a atualizar.
        saldo (float): novo saldo do utilizador.
        historico (list): nova lista de movimentos do utilizador.
    """

    dados = carregar_dados()
    for utilizador in dados:
        if utilizador["Username"] == username:
            utilizador["Saldo"] = saldo
            utilizador["Historico"] = historico
            break
    guardar_dados(dados)
