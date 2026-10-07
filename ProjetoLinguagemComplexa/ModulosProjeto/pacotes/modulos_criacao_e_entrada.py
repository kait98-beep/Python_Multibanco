from ModulosProjeto.pacotes import (
    modulo_dados_e_classes,
    modulos_file_manipulation,
    modulos_excecoes
)

def criar_utilizador():
    """Permite criar o username e password do utilizador e guarda a 
        informação no dados_guardados.json.

    Raises:
        modulos_excecoes.UtilizadorJaExisteError: se o username já existir 
        nos dados_guardados.json ou dados_utilizador
    """
    user_validacao = False
    pass_validacao = False

    while user_validacao is False:
        username = input("Insira um username: ")

        if modulos_file_manipulation.encontrar_utilizador(username) is None:
            print("Username criada com sucesso\n")

            while pass_validacao is False:
                password = input("Insira um password: ")
                # Tamanho compreendido entre 6 - 10; Necessita de, pelo menos, 1 número e 1 caracter
                if (
                    len(password) >= 6
                    and len(password) <= 10
                    and any(char.isdigit() for char in password)
                    and any(char.isalpha() for char in password)
                ):
                    print("Password criada com sucesso\n")

                    modulos_file_manipulation.adicionar_utilizador(
                        username=username,
                        password=password
                    )
                    pass_validacao = True
                else:
                    print("Password não apresenta todos os critérios solicitados!\n")
            user_validacao = True
        else:
            raise modulos_excecoes.UtilizadorJaExisteError("Username já existe!")

def entrar():
    """Realiza a validação dos dados, tanto do username como do password, para o utilizador
    poder aceder à sua conta no banco.
    """
    validacao = False
    while validacao is False:
        username = input("Insira o username: ")
        password = input("Insira o password: ")
        utilizador_guardado = modulos_file_manipulation.encontrar_utilizador(username)

        if utilizador_guardado is None or utilizador_guardado["Password"] != password:
            print("Dados errados inseridos")
            break
        else:
            print("Dados inseridos corretamente.\n")
            # Carregar a conta
            modulo_dados_e_classes.UTILIZADOR_ATUAL = username
            validacao = True
