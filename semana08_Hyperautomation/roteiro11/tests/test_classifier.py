from pathlib import Path

from src.modules.classificacao import classificar_documentos


def test_classificar_documento_aprovado(tmp_path):
    origem = tmp_path / "origem"
    pasta_ok = tmp_path / "Documentos_OK"
    pasta_pendentes = tmp_path / "Documentos_Pendentes"

    origem.mkdir()

    arquivo = origem / "documento.pdf"
    arquivo.write_text("arquivo de teste")

    destino = classificar_documentos(
        arquivos=[arquivo],
        aprovado=True,
        pasta_ok=pasta_ok,
        pasta_pendentes=pasta_pendentes,
    )

    assert destino == pasta_ok
    assert (pasta_ok / "documento.pdf").exists()


def test_classificar_documento_pendente(tmp_path):
    origem = tmp_path / "origem"
    pasta_ok = tmp_path / "Documentos_OK"
    pasta_pendentes = tmp_path / "Documentos_Pendentes"

    origem.mkdir()

    arquivo = origem / "documento.pdf"
    arquivo.write_text("arquivo de teste")

    destino = classificar_documentos(
        arquivos=[arquivo],
        aprovado=False,
        pasta_ok=pasta_ok,
        pasta_pendentes=pasta_pendentes,
    )

    assert destino == pasta_pendentes
    assert (pasta_pendentes / "documento.pdf").exists()
