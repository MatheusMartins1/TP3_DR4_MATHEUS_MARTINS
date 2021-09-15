import socket
from CONSTANTS import *

PORTA = PORTA - 1109
arquivo = 'noite.jpg'
comando = {}

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    print(f"Realizando conexão {HOST} na porta {PORTA}")
    tcp.connect((HOST, PORTA))

    print(f"Solicitando tamanho do arquivo: {arquivo}")
    comando[0] = arquivo
    comando[1] = "info"
    comando_byte = pickle.dumps(comando)
    tcp.send(comando_byte)

    resposta = tcp.recv(4096)
    info_arquivo = pickle.loads(resposta, fix_imports=True, encoding="utf-8")

    if info_arquivo['Tamanho'] != 0:
        print("\nResposta:", json.dumps(info_arquivo, indent=4, sort_keys=True))

        comando[1] = "arquivo"
        comando_byte = pickle.dumps(comando)

        print(f"Solicitando o download do arquivo | comando {comando}")
        tcp.send(comando_byte)

        nome_split = arquivo.split(".")
        nome_arquivo = f'arquivos//{nome_split[0]}_baixado.{nome_split[1]}'

        print(f'\nGerando arquivo {nome_arquivo} com tamanho {info_arquivo["Tamanho"]}')
        with open(nome_arquivo, "wb+") as arquivo_novo:
            soma = 0
            arq_bytes = tcp.recv(1024)

            while arq_bytes:
                arquivo_novo.write(arq_bytes)
                soma = soma + len(arq_bytes)
                print(f"Baixando...{soma}KB de {info_arquivo['Tamanho']}KB")
                arq_bytes = tcp.recv(1024)

        arquivo_novo.close()
        print(f"arquivo {nome_arquivo} baixado")

    else:
        print("Arquivo Inválido")

except Exception as erro:
    print("erro:",str(erro))

tcp.close()


