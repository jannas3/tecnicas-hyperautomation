import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv


def enviar_resposta(
    destinatario: str,
    assunto: str,
    corpo: str,
) -> None:
    """
    Envia a resposta do processamento ao cliente.
    """

    load_dotenv()

    remetente = os.getenv("EMAIL_REMETENTE")
    senha = os.getenv("EMAIL_SENHA")

    smtp_host = os.getenv(
        "SMTP_HOST",
        "smtp.gmail.com",
    )

    smtp_port = int(
        os.getenv(
            "SMTP_PORT",
            "587",
        )
    )

    if not remetente or not senha:
        raise ValueError("Credenciais SMTP não configuradas no .env")

    if not destinatario:
        raise ValueError("Destinatário do e-mail não informado.")

    mensagem = MIMEMultipart()

    mensagem["From"] = remetente
    mensagem["To"] = destinatario
    mensagem["Subject"] = assunto

    mensagem.attach(
        MIMEText(
            corpo,
            "plain",
            "utf-8",
        )
    )

    with smtplib.SMTP(
        smtp_host,
        smtp_port,
    ) as servidor:

        servidor.ehlo()
        servidor.starttls()
        servidor.ehlo()

        servidor.login(
            remetente,
            senha,
        )

        servidor.send_message(mensagem)
