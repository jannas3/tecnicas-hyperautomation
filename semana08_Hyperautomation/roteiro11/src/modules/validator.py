import re


def limpar_cpf(cpf: str) -> str:
    """Remove pontos, traços e qualquer caractere não numérico."""
    return re.sub(r"\D", "", cpf)


def validar_cpf(cpf: str) -> bool:
    """Valida CPF pelos dígitos verificadores."""

    cpf = limpar_cpf(cpf)

    if len(cpf) != 11:
        return False

    if cpf == cpf[0] * 11:
        return False

    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = (soma * 10) % 11

    if digito1 == 10:
        digito1 = 0

    if digito1 != int(cpf[9]):
        return False

    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma * 10) % 11

    if digito2 == 10:
        digito2 = 0

    return digito2 == int(cpf[10])


def validar_campos_obrigatorios(dados: dict) -> tuple[bool, str]:
    """Verifica se os campos obrigatórios estão preenchidos."""

    campos = [
        "cpf",
        "nome",
        "data_nascimento",
        "endereco",
        "email",
        "telefone",
    ]

    for campo in campos:
        if not dados.get(campo):
            return False, f"Campo obrigatório ausente: {campo}"

    if not validar_cpf(dados["cpf"]):
        return False, "CPF inválido"

    return True, "Dados válidos"
