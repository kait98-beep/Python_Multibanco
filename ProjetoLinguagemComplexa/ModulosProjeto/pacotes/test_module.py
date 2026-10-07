import os
import pytest
from ModulosProjeto.pacotes import (
    modulo_dados_e_classes,
    modulos_criacao_e_entrada,
    modulos_excecoes,
    modulos_file_manipulation,
    modulos_funcoes_no_banco
)

def test_utilizador_duplicado(monkeypatch):
    """Verifica que criar um utilizador com um username já existente
    levanta UtilizadorJaExisteError.

    Args:
        monkeypatch (pytest.MonkeyPatch): usado para trocar o ficheiro JSON
        e simular o input do utilizador.
    """

    monkeypatch.setattr(modulos_file_manipulation, "FILE_PATH", "teste.json")
    modulos_file_manipulation.adicionar_utilizador("diogo", "abc123456")

    respostas = iter(["diogo"])
    monkeypatch.setattr("builtins.input", lambda _: next(respostas))

    with pytest.raises(modulos_excecoes.UtilizadorJaExisteError):
        modulos_criacao_e_entrada.criar_utilizador()

def test_utilizador_inexistente_transferencia(monkeypatch):
    """Verifica que transferir para um utilizador que não existe
    levanta UtilizadorInexistenteError.

    Args:
        monkeypatch (pytest.MonkeyPatch): usado para trocar o ficheiro JSON,
        definir o utilizador logado e simular o input.
    """

    monkeypatch.setattr(modulos_file_manipulation, "FILE_PATH","teste.json")
    if os.path.exists("teste.json"):
        os.remove("teste.json")

    modulos_file_manipulation.adicionar_utilizador("diogo", "abc123456")
    modulos_file_manipulation.adicionar_utilizador("ana", "abc123456")
    modulos_file_manipulation.atualizar_utilizador("diogo", 100, [])

    monkeypatch.setattr(modulo_dados_e_classes, "UTILIZADOR_ATUAL", "diogo")

    respostas = iter(["Zeca", "50"])  # [valor, opção inválida]
    monkeypatch.setattr("builtins.input", lambda _: next(respostas))

    with pytest.raises(modulos_excecoes.UtilizadorInexistenteError):
        modulos_funcoes_no_banco.transferencia()


def test_transferencia_sucesso(monkeypatch, capsys):
    """Verifica que uma transferência válida termina com a mensagem de sucesso.

    Args:
        monkeypatch (pytest.MonkeyPatch): usado para trocar o ficheiro JSON,
        definir o utilizador logado e simular o input.
        capsys (pytest.CaptureFixture): usado para ler o que foi impresso.
    """

    monkeypatch.setattr(modulos_file_manipulation, "FILE_PATH", "texto.json")
    modulos_file_manipulation.adicionar_utilizador("diogo", "abc123456")
    modulos_file_manipulation.adicionar_utilizador("ana", "abc123456")
    modulos_file_manipulation.atualizar_utilizador("diogo", 100, [])

    monkeypatch.setattr(modulo_dados_e_classes, "UTILIZADOR_ATUAL", "diogo")

    respostas = iter(["ana", "50"])  # valor, opção 1 = ana
    monkeypatch.setattr("builtins.input", lambda _: next(respostas))

    modulos_funcoes_no_banco.transferencia()

    saida = capsys.readouterr().out
    assert "Transferência concluída com sucesso" in saida


def test_saldo_insuficiente(monkeypatch):
    """Verifica que transferir mais do que o saldo disponível
    levanta SaldoInsuficienteError.

    Args:
        monkeypatch (pytest.MonkeyPatch): usado para trocar o ficheiro JSON,
        definir o utilizador logado e simular o input.
    """

    monkeypatch.setattr(modulos_file_manipulation, "FILE_PATH", "teste.json")
    modulos_file_manipulation.adicionar_utilizador("diogo", "abc123456")
    modulos_file_manipulation.atualizar_utilizador("diogo", 10, [])
    monkeypatch.setattr(modulo_dados_e_classes, "UTILIZADOR_ATUAL", "diogo")

    respostas = iter(["ana", "50"])
    monkeypatch.setattr("builtins.input", lambda _: next(respostas))

    with pytest.raises(modulos_excecoes.SaldoInsuficienteError):
        modulos_funcoes_no_banco.transferencia()

if __name__ == "__main__":
    pytest.main()
