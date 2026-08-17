import email
import imaplib
import os
import re
from datetime import datetime
from email.header import decode_header
from pathlib import Path

from dotenv import load_dotenv


def decodificar_cabecalho(valor: str) -> str:
    partes = decode_header(valor)
    resultado = []

    for parte, encoding in partes:
        if isinstance(parte, bytes):
            resultado.append(
                parte.decode(encoding or "utf-8", errors="replace")
            )
        else:
            resultado.append(parte)

    return "".join(resultado)


def sanitizar_nome(nome: str) -> str:
    return re.sub(r"[^\w\-_. ]", "_", nome).strip()


def receber_solicitacoes(pasta_automacao: Path) -> list[dict]:
    load_dotenv()

    imap_host = os.getenv("IMAP_HOST", "imap.gmail.com")
    imap_port = int(os.getenv("IMAP_PORT", "993"))

    imap_user = os.getenv("IMAP_USER")
    imap_password = os.getenv("IMAP_PASSWORD")

    filtro_assunto = os.getenv(
        "IMAP_FILTRO_ASSUNTO",
        "Cadastro Portal Fake"
    )

    if not imap_user or not imap_password:
        raise ValueError(
            "Credenciais IMAP não configuradas no arquivo .env"
        )

    pasta_downloads = pasta_automacao / "Downloads"
    pasta_downloads.mkdir(parents=True, exist_ok=True)

    solicitacoes = []

    with imaplib.IMAP4_SSL(
        imap_host,
        imap_port
    ) as servidor:

        servidor.login(
            imap_user,
            imap_password
        )

        servidor.select("INBOX")

        criterio = (
            f'UNSEEN SUBJECT "{filtro_assunto}"'
        )

        status, dados = servidor.search(
            None,
            criterio
        )

        if status != "OK":
            return []

        ids = dados[0].split()

        for msg_id in ids:

            _, dados_msg = servidor.fetch(
                msg_id,
                "(BODY.PEEK[])"
            )

            mensagem = email.message_from_bytes(
                dados_msg[0][1]
            )

            remetente_raw = decodificar_cabecalho(
                mensagem.get("From", "")
            )

            assunto = decodificar_cabecalho(
                mensagem.get("Subject", "")
            )

            resultado_email = re.search(
                r"[\w.\-+]+@[\w.\-]+",
                remetente_raw
            )

            remetente = (
                resultado_email.group(0)
                if resultado_email
                else remetente_raw
            )

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            id_solicitacao = sanitizar_nome(
                f"{timestamp}_{remetente}"
            )

            pasta_solicitacao = (
                pasta_downloads
                / id_solicitacao
            )

            pasta_solicitacao.mkdir(
                parents=True,
                exist_ok=True
            )

            anexos = []

            for parte in mensagem.walk():

                content_disp = (
                    parte.get(
                        "Content-Disposition",
                        ""
                    )
                )

                if "attachment" not in content_disp:
                    continue

                nome = parte.get_filename()

                if not nome:
                    continue

                nome = decodificar_cabecalho(nome)
                nome = sanitizar_nome(nome)

                payload = parte.get_payload(
                    decode=True
                )

                if payload:
                    caminho = (
                        pasta_solicitacao
                        / nome
                    )

                    caminho.write_bytes(payload)

                    anexos.append(nome)

            if anexos:
                solicitacoes.append(
                    {
                        "id_solicitacao": id_solicitacao,
                        "remetente": remetente,
                        "assunto": assunto,
                        "pasta_downloads": pasta_solicitacao,
                        "anexos": anexos,
                    }
                )

                servidor.store(
                    msg_id,
                    "+FLAGS",
                    "\\Seen"
                )

    return solicitacoes