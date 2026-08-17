from pathlib import Path

from src.modules.leitura_email import receber_solicitacoes
from src.modules.validacao_documentos import validar_documentacao
from src.modules.extracao import localizar_ficha, extrair_dados_ficha
from src.modules.validator import validar_campos_obrigatorios
from src.modules.classificacao import classificar_documentos
from src.modules.spreadsheet import registrar_cadastro
from src.modules.resposta_cliente import enviar_resposta


# ==========================================================
# CONFIGURAÇÕES DE PASTAS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PASTA_AUTOMACAO = BASE_DIR / "Projeto_Automacao"

PASTA_DOWNLOADS = PASTA_AUTOMACAO / "Downloads"
PASTA_OK = PASTA_AUTOMACAO / "Documentos_OK"
PASTA_PENDENTES = PASTA_AUTOMACAO / "Documentos_Pendentes"

PLANILHA_MESTRA = PASTA_AUTOMACAO / "Planilha_Mestra.xlsx"


# ==========================================================
# PROCESSAR UMA SOLICITAÇÃO
# ==========================================================

def processar_solicitacao(solicitacao: dict) -> None:

    print("\n" + "=" * 60)
    print(
        f"Processando solicitação: "
        f"{solicitacao['id_solicitacao']}"
    )
    print("=" * 60)

    pasta_solicitacao = Path(
        solicitacao["pasta_downloads"]
    )

    anexos = solicitacao["anexos"]

    # --------------------------------------------------
    # 1. VALIDAR DOCUMENTAÇÃO
    # --------------------------------------------------

    print("\n[1] Validando documentação...")

    resultado_documentos = validar_documentacao(
        anexos
    )

    if not resultado_documentos["completa"]:

        motivo = (
            "Documentos ausentes: "
            + ", ".join(
                resultado_documentos["pendentes"]
            )
        )

        print(f"PENDENTE: {motivo}")

        arquivos = list(
            pasta_solicitacao.iterdir()
        )

        classificar_documentos(
            arquivos=arquivos,
            aprovado=False,
            pasta_ok=PASTA_OK,
            pasta_pendentes=PASTA_PENDENTES,
        )

        print(
            "Documentos enviados para "
            "Documentos_Pendentes."
        )

        # Resposta ao cliente
        print(
            "\nEnviando resposta de pendência "
            "ao cliente..."
        )

        enviar_resposta(
            destinatario=solicitacao["remetente"],
            assunto="Pendência no Cadastro - Portal Fake",
            corpo=(
                "Olá,\n\n"
                "Não foi possível concluir seu cadastro.\n\n"
                f"Motivo: {motivo}\n\n"
                "Por favor, envie novamente os "
                "documentos necessários.\n\n"
                "Portal Fake Soluções Digitais"
            ),
        )

        print(
            "E-mail de pendência enviado ao cliente."
        )

        return

    print("Documentação completa.")

    # --------------------------------------------------
    # 2. LOCALIZAR FICHA
    # --------------------------------------------------

    print("\n[2] Localizando ficha...")

    ficha = localizar_ficha(
        pasta_solicitacao
    )

    print(
        f"Ficha encontrada: {ficha.name}"
    )

    # --------------------------------------------------
    # 3. EXTRAIR DADOS
    # --------------------------------------------------

    print("\n[3] Extraindo dados da ficha...")

    dados = extrair_dados_ficha(
        ficha
    )

    print("Dados extraídos:")
    print(dados)

    # --------------------------------------------------
    # 4. VALIDAR DADOS
    # --------------------------------------------------

    print("\n[4] Validando dados...")

    valido, motivo = (
        validar_campos_obrigatorios(dados)
    )

    if not valido:

        print(
            f"PENDENTE: {motivo}"
        )

        arquivos = list(
            pasta_solicitacao.iterdir()
        )

        classificar_documentos(
            arquivos=arquivos,
            aprovado=False,
            pasta_ok=PASTA_OK,
            pasta_pendentes=PASTA_PENDENTES,
        )

        print(
            "Documentos enviados para "
            "Documentos_Pendentes."
        )

        # Resposta ao cliente
        print(
            "\nEnviando resposta de pendência "
            "ao cliente..."
        )

        enviar_resposta(
            destinatario=solicitacao["remetente"],
            assunto="Pendência no Cadastro - Portal Fake",
            corpo=(
                "Olá,\n\n"
                "Identificamos uma pendência "
                "em seu cadastro.\n\n"
                f"Motivo: {motivo}\n\n"
                "Por favor, verifique os dados "
                "e envie novamente a solicitação.\n\n"
                "Portal Fake Soluções Digitais"
            ),
        )

        print(
            "E-mail de pendência enviado ao cliente."
        )

        return

    print("Dados válidos.")

    # --------------------------------------------------
    # 5. REGISTRAR NA PLANILHA
    # --------------------------------------------------

    print(
        "\n[5] Atualizando Planilha Mestra..."
    )

    registrar_cadastro(
        dados=dados,
        caminho_planilha=PLANILHA_MESTRA,
    )

    print(
        "Cadastro registrado na Planilha Mestra."
    )

    # --------------------------------------------------
    # 6. CLASSIFICAR DOCUMENTOS
    # --------------------------------------------------

    print(
        "\n[6] Arquivando documentos..."
    )

    arquivos = list(
        pasta_solicitacao.iterdir()
    )

    classificar_documentos(
        arquivos=arquivos,
        aprovado=True,
        pasta_ok=PASTA_OK,
        pasta_pendentes=PASTA_PENDENTES,
    )

    print(
        "Documentos enviados para Documentos_OK."
    )

    # --------------------------------------------------
    # 7. RESPONDER AO CLIENTE
    # --------------------------------------------------

    print(
        "\n[7] Enviando resposta ao cliente..."
    )

    enviar_resposta(
        destinatario=solicitacao["remetente"],
        assunto="Cadastro Aprovado - Portal Fake",
        corpo=(
            f"Olá, {dados['nome']}!\n\n"
            "Seu cadastro foi processado e "
            "aprovado com sucesso.\n\n"
            "Portal Fake Soluções Digitais"
        ),
    )

    print(
        "E-mail de aprovação enviado ao cliente."
    )

    print(
        "\nCadastro processado com sucesso."
    )


# ==========================================================
# EXECUÇÃO PRINCIPAL
# ==========================================================

def main() -> None:

    print("=" * 60)
    print(
        "AUTOMAÇÃO DE CADASTROS - PORTAL FAKE"
    )
    print("=" * 60)

    # Garante que as pastas existam
    PASTA_DOWNLOADS.mkdir(
        parents=True,
        exist_ok=True
    )

    PASTA_OK.mkdir(
        parents=True,
        exist_ok=True
    )

    PASTA_PENDENTES.mkdir(
        parents=True,
        exist_ok=True
    )

    try:

        # ------------------------------------------------
        # 1. ACESSAR E-MAIL
        # ------------------------------------------------

        print(
            "\nAcessando caixa de e-mail..."
        )

        solicitacoes = receber_solicitacoes(
            PASTA_AUTOMACAO
        )

        if not solicitacoes:

            print(
                "Nenhuma nova solicitação encontrada."
            )

            return

        print(
            f"{len(solicitacoes)} "
            "solicitação(ões) encontrada(s)."
        )

        # ------------------------------------------------
        # 2. PROCESSAR SOLICITAÇÕES
        # ------------------------------------------------

        for solicitacao in solicitacoes:

            try:

                processar_solicitacao(
                    solicitacao
                )

            except PermissionError:

                print(
                    "\nERRO: Não foi possível acessar "
                    "a Planilha Mestra."
                )

                print(
                    "Verifique se o arquivo está aberto "
                    "no Excel e tente novamente."
                )

            except FileNotFoundError as erro:

                print(
                    "\nErro de arquivo:"
                )

                print(erro)

            except ValueError as erro:

                print(
                    "\nErro de validação:"
                )

                print(erro)

            except Exception as erro:

                print(
                    "\nErro ao processar "
                    "a solicitação:"
                )

                print(erro)

    except ConnectionError as erro:

        print(
            "\nErro de conexão:"
        )

        print(erro)

    except Exception as erro:

        print(
            "\nErro durante execução "
            "da automação:"
        )

        print(erro)

    finally:

        print(
            "\n" + "=" * 60
        )

        print(
            "EXECUÇÃO FINALIZADA"
        )

        print(
            "=" * 60
        )


# ==========================================================
# INICIAR PROGRAMA
# ==========================================================

if __name__ == "__main__":
    main()