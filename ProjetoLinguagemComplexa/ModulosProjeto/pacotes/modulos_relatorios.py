import multiprocessing
from ModulosProjeto.pacotes import modulos_funcoes_no_banco, modulos_file_manipulation

def gerar_relatorio_saldos():
    """Fornecer um relatório com os utilizadores com maior saldo, 
        com menor saldo e a soma de todos os saldos
    """

    dados = modulos_file_manipulation.carregar_dados()
    lista_numeros = [] # Para o sum
    lista_user_saldo_maior = []
    lista_user_saldo_menor = []
    maior_saldo = 0
    menor_saldo = 0
    soma = 0

    for i in dados:
        lista_numeros.append(i["Saldo"]) # Soma
        maior_saldo = max(lista_numeros)
        menor_saldo = min(lista_numeros)
        soma = sum(lista_numeros)
    for y in dados:
        if y["Saldo"] == maior_saldo:
            lista_user_saldo_maior.append(y["Username"])
        if y["Saldo"] == menor_saldo:
            lista_user_saldo_menor.append(y["Username"])

    print(f"Utilizador/es {lista_user_saldo_maior} com maior saldo: {maior_saldo}")
    print(f"Utilizador/es {lista_user_saldo_menor} com menor saldo: {menor_saldo}")
    print(f"Soma de todos os saldos: {soma}")

def gerar_relatorio_transferencias():
    """Fornecer um relatório com os utilizadores 
        que mais dinheiro receberam, mais dinheiro enviaram
        e a soma total do dinheiro transferido
    """

    dados = modulos_file_manipulation.carregar_dados()
    dic_enviados = {}
    dic_recebidos = {}
    total_transferido = 0.0

    for i in dados:
        nome = i["Username"]
        dic_enviados[nome] = 0.0
        dic_recebidos[nome] = 0.0

        for y in i["Historico"]:
            palavras = y.split()
            palavra_chave = palavras[1]

            if palavra_chave == "enviado":
                numero_texto = float(palavras[-1])
                dic_enviados[nome] += numero_texto
                total_transferido += numero_texto

            elif palavra_chave == "recebido":
                numero_texto = float(palavras[-1])
                dic_recebidos[nome] += numero_texto

    max_enviado = 0.0
    maximo_enviado = []

    for user_max_enviado in dic_enviados:
        if dic_enviados[user_max_enviado] > max_enviado:
            max_enviado = dic_enviados[user_max_enviado]
            maximo_enviado = [user_max_enviado]
        elif dic_enviados[user_max_enviado] == max_enviado and max_enviado > 0:
            maximo_enviado.append(user_max_enviado)

    max_recebido = 0.0
    maximo_recebido = []

    for user_max_recebeu in dic_recebidos:
        if dic_recebidos[user_max_recebeu] > max_recebido:
            max_recebido = dic_recebidos[user_max_recebeu]
            maximo_recebido = [user_max_recebeu]
        elif dic_enviados[user_max_recebeu] == max_recebido and max_recebido > 0:
            maximo_enviado.append(user_max_recebeu)

    print(f"Utilizador/es que mais dinheiro recebeu/receberam: {maximo_recebido}")
    print(f"Utilizador/es que mais dinheiro enviou/enviaram: {maximo_enviado}")
    print(f"Soma de todo o dinheiro transferido: {total_transferido}")


if __name__ == "__main__":
    processo_1 = multiprocessing.Process(target=gerar_relatorio_saldos)
    processo_2 = multiprocessing.Process(target=gerar_relatorio_transferencias)

    processo_1.start()
    processo_2.start()
    processo_1.join()
    processo_2.join()

def consultar_transferencias():
    """Consultar as transferências onde o próprio utilizado está envolvido

    Returns:
        list | None: transferências do utilizador logado (sem depósitos),
        ordenadas por valor. Devolve None se a opção de ordenação for inválida.
    """

    conta_logada = modulos_funcoes_no_banco.conta_atual()
    tamanho = len(conta_logada.historico)
    ordem = int(input(
        "Como quer ordenar a lista das transferências:\n"
        " 1 - Crescente "
        " 2 - Decrescente "
    ))
    if ordem == 1:
        for i in range(tamanho - 1):
            m = i
            for j in range(i + 1, tamanho):
                if (
                    float(conta_logada.historico[j].split()[-1])
                    < float(conta_logada.historico[m].split()[-1])
                ):
                    m = j

            conta_logada.historico[i], conta_logada.historico[m] = conta_logada.historico[m], conta_logada.historico[i]

        lista_1 = []

        for y in conta_logada.historico:
            palavras = y.split()
            palavra_chave = palavras[0]

            if palavra_chave != "Deposito":
                lista_1.append(y)
        return lista_1

    elif ordem == 2:
        for i in range(tamanho - 1):
            m = i
            for j in range(i + 1, tamanho):
                if (
                    float(conta_logada.historico[j].split()[-1])
                    > float(conta_logada.historico[m].split()[-1])
                ):
                    m = j

            conta_logada.historico[i], conta_logada.historico[m] = conta_logada.historico[m], conta_logada.historico[i]

        lista_2 = []

        for y in conta_logada.historico:
            palavras = y.split()
            palavra_chave = palavras[0]

            if palavra_chave != "Deposito":
                lista_2.append(y)
        return lista_2

    else:
        print("Número introduzido errado")
