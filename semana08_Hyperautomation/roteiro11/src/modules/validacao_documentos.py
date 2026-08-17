from pathlib import Path


DOCUMENTOS_OBRIGATORIOS = {
    "documento_identidade": [
        "documento",
        "foto",
        "rg",
        "cnh",
        "identidade",
    ],

    "comprovante_residencia": [
        "comprovante",
        "residencia",
        "endereco",
    ],

    "ficha_cadastro": [
        "ficha",
        "cadastro",
    ],
}


def validar_documentacao(
    anexos: list[str]
) -> dict:

    encontrados = {}
    pendentes = []

    for categoria, palavras in (
        DOCUMENTOS_OBRIGATORIOS.items()
    ):

        arquivo_encontrado = None

        for arquivo in anexos:

            nome = arquivo.lower()

            if any(
                palavra in nome
                for palavra in palavras
            ):
                arquivo_encontrado = arquivo
                break

        encontrados[categoria] = (
            arquivo_encontrado
        )

        if arquivo_encontrado is None:
            pendentes.append(categoria)

    return {
        "completa": len(pendentes) == 0,
        "pendentes": pendentes,
        "detalhes": encontrados,
    }