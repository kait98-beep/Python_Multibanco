import pyfiglet
from ModulosProjeto.pacotes import (
    modulos_criacao_e_entrada,
    modulos_funcoes_no_banco,
    modulos_file_manipulation,
    modulos_excecoes,
    modulos_relatorios,
    modulo_dados_e_classes
)

# Apresentação do Menu
while True:
    pyfiglet.print_figlet("Banco Pereira")
    input_utilizador = int(input(
        "Introduza um dos seguintes valores:\n"
        " 0 - Sair do programa\n"
        " 1 - Criar utilizador\n"
        " 2 - Entrar\n"
        "Valor Introduzido: "
    ))

    match(input_utilizador):
        case 0:
            print("Sair do programa")
            pyfiglet.print_figlet(". . . . . .")
            break
        case 1:
            try:
                modulos_criacao_e_entrada.criar_utilizador()
                print("Conta criada com sucesso!")
            except modulos_excecoes.UtilizadorJaExisteError as username:
                print(username)
        case 2:
            if not modulos_file_manipulation.carregar_dados():
                print("Não existe utilizador nenhum")
            else:
                modulo_dados_e_classes.UTILIZADOR_ATUAL = None
                modulos_criacao_e_entrada.entrar()

                if modulo_dados_e_classes.UTILIZADOR_ATUAL is not None:
                    while True:
                        pyfiglet.print_figlet("Conta")
                        input_utilizador2 = int(input(
                            "Introduza um dos seguintes valores:\n"
                            " 0 - Sair da conta\n"
                            " 3 - Depositar dinheiro\n"
                            " 4 - Consultar saldo\n"
                            " 5 - Transferir dinheiro\n"
                            " 6 - Consultar retorno\n"
                            " 7 - Gerar Relatório\n"
                            " 8 - Consultar Transferencias\n"
                            "Valor Introduzido: "
                        ))
                        match(input_utilizador2):
                            case 3:
                                modulos_funcoes_no_banco.depositar()

                            case 4:
                                print(modulos_funcoes_no_banco.consultar_saldo())

                            case 5:
                                try:
                                    modulos_funcoes_no_banco.transferencia()
                                except modulos_excecoes.SaldoInsuficienteError as saldo:
                                    print(saldo)
                                except modulos_excecoes.UtilizadorInexistenteError as utilizador:
                                    print(utilizador)
                                except modulos_excecoes.ProprioUtilizadorError as proprio:
                                    print(proprio)
                            case 6:
                                taxa_juro = float(input("Insira um valor de Juro entre 0 e 100: "))
                                numero_meses = int(input("Insira o numero de meses de 1 a 12: "))
                                print(
                                    "O valor com juro é:",
                                    modulos_funcoes_no_banco.consultar_retorno(
                                        numero_meses=numero_meses, taxa_juro=taxa_juro
                                    )
                                )
                            case 7:
                                modulos_relatorios.gerar_relatorio_saldos()
                                modulos_relatorios.gerar_relatorio_transferencias()
                            case 8:
                                print(modulos_relatorios.consultar_transferencias())
                            case 0:
                                print("Saiu da conta")
                                break
                            case _:
                                print("Opção inválida. Tente novamente.\n")
        case _:
            print("Opção inválida. Tente novamente.\n")
