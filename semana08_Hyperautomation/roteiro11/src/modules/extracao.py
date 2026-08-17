import re
from pathlib import Path

from docx import Document


def limpar_email(email: str) -> str:
    """
    Remove formatação de link e retorna somente o endereço de e-mail.
    """

    email = email.strip()

    inicio = email.find("[")
    fim = email.find("]")

    if inicio != -1 and fim != -1 and fim > inicio:
        endereco = email[inicio + 1:fim].strip()

        if "@" in endereco:
            return endereco

    if "mailto:" in email:
        endereco = email.split("mailto:", 1)[1]
        endereco = endereco.split(")", 1)[0]
        endereco = endereco.replace("\\", "").strip()

        if "@" in endereco:
            return endereco

    return email.replace("\\", "").strip()
def localizar_ficha(
    pasta_solicitacao: Path
) -> Path:

    for arquivo in pasta_solicitacao.iterdir():

        nome = arquivo.name.lower()

        if (
            "ficha" in nome
            and arquivo.suffix.lower() == ".docx"
        ):
            return arquivo

    raise FileNotFoundError(
        "Ficha de cadastro não encontrada."
    )
def extrair_dados_ficha(caminho_ficha: Path) -> dict:
    if not caminho_ficha.exists():
        raise FileNotFoundError(f"Ficha de cadastro não encontrada: {caminho_ficha}")

    documento = Document(caminho_ficha)

    dados = {}

    mapa_campos = {
        "nome": "nome",
        "cpf": "cpf",
        "e-mail": "email",
        "telefone": "telefone",
        "data de nascimento": "data_nascimento",
        "endereço": "endereco",
    }

    for tabela in documento.tables:
        for linha in tabela.rows:

            if len(linha.cells) < 2:
                continue

            campo = linha.cells[0].text.strip().lower()
            valor = linha.cells[1].text.strip()

            if campo in mapa_campos:
                dados[mapa_campos[campo]] = valor

    if "email" in dados:
        dados["email"] = limpar_email(dados["email"])

    return dados
