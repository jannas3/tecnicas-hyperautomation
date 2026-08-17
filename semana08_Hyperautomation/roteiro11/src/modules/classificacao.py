from pathlib import Path
import shutil


def classificar_documentos(
    arquivos: list[Path],
    aprovado: bool,
    pasta_ok: Path,
    pasta_pendentes: Path,
):
    destino = pasta_ok if aprovado else pasta_pendentes

    destino.mkdir(parents=True, exist_ok=True)

    for arquivo in arquivos:

        if not arquivo.exists():
            raise FileNotFoundError(
                f"Arquivo não encontrado: {arquivo}"
            )

        shutil.move(
            str(arquivo),
            str(destino / arquivo.name),
        )

    return destino