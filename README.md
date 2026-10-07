# Python_Multibanco
Máquina de multibanco com persistência de dados desenvolvido em âmbito de CET

Banco Pereira:
Aplicação de banco em linha de comandos, escrita em Python, desenvolvida no âmbito do projeto de Linguagem Complexa. Permite criar contas, fazer depósitos e transferências entre utilizadores, simular retornos com juro composto e consultar relatórios. Os dados ficam guardados num ficheiro JSON.

>> Menu Inicial:
0: Sair do Programa
1: Criar utilizador
2: Entrar numa conta

Após entrar numa conta

>> Menu da Conta:
0: Sair da conta
3: Depositar dinheiro
4: Consultar saldo
5: Transferir dinheiro para outro utilizador
6: Consultar retorno (com juro composto)
7: Gerar relatórios (saldos e transferências)
8: Consultar as minhas transferências (ordenadas por valor)

>> Regras e validações:
- Username: tem de ser único.
- Password: entre 6 e 10 caracteres, com pelo menos 1 letra e 1 número.
- Depósitos e transferências: o valor tem de ser superior a zero.
- Transferências: não é possível transferir para a própria conta, para um utilizador inexistente ou com saldo insuficiente. Cada transferência fica registada no histórico de ambas as contas, com data e hora.
- Retorno: taxa de juro mensal entre 0 e 100 (%) e número de meses entre 1 e 12, calculado de forma recursiva.
- Relatório de saldos: utilizador(es) com maior e menor saldo e soma de todos os saldos.
- Relatório de transferências: utilizador(es) que mais enviaram e receberam e total transferido. Os dois relatórios podem ser executados em paralelo com multiprocessing (ao correr modulos_relatorios.py diretamente).

>> Estrutura do código:
ProjetoLinguagemComplexa/
|--- projeto_final.py
|--- dados_guardados.json
|--- ModulosProjeto/
      |-- pacotes/
            |-- modulo_dados_e_classes.py
            |-- modulos_criacao_e_entrada.py
            |-- modulos_file_manipulation.py
            |-- modulos_funcoes_no_banco.py
            |-- modulos_relatorios.py
            |-- modulos_excecoes.py
            |-- test_module.py

>> Requisitos:
- Python 3.10 ou superior (o projeto usa match/case)
- pyfiglet – títulos em ASCII art
- pytest – apenas para correr os testes

>> Os testes:
- Criação de um utilizador com username duplicado;
- Transferência para um utilizador inexistente;
- Transferência concluída com sucesso;
- Transferência com saldo insuficiente.

>> Formato dos dados:
Cada utilizador é guardado em dados_guardados.json

>> Exceções personalizadas:
- UtilizadorJaExisteError:	Ao criar um utilizador com um username já existente
- UtilizadorInexistenteError:	Ao transferir para um username que não existe
- SaldoInsuficienteError:	Ao transferir um valor superior ao saldo
- ProprioUtilizadorError:	Ao tentar transferir para a própria conta

>> Limitações:
- As passwords são guardados em texto simples no JSON
- O menu não trata entradas não numéricas
