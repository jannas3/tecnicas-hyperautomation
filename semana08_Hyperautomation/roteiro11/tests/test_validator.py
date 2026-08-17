from src.modules.validator import validar_cpf, validar_campos_obrigatorios


def test_cpf_valido():
    assert validar_cpf("529.982.247-25") is True


def test_cpf_invalido():
    assert validar_cpf("111.111.111-11") is False


def test_campos_obrigatorios_validos():
    dados = {
        "cpf": "52998224725",
        "nome": "Maria Silva",
        "data_nascimento": "10/05/1995",
        "endereco": "Rua A, 100",
        "email": "maria@email.com",
        "telefone": "92999999999",
    }

    valido, mensagem = validar_campos_obrigatorios(dados)

    assert valido is True
    assert mensagem == "Dados válidos"


def test_nome_ausente():
    dados = {
        "cpf": "52998224725",
        "nome": "",
        "data_nascimento": "10/05/1995",
        "endereco": "Rua A, 100",
        "email": "maria@email.com",
        "telefone": "92999999999",
    }

    valido, mensagem = validar_campos_obrigatorios(dados)

    assert valido is False
    assert "nome" in mensagem
