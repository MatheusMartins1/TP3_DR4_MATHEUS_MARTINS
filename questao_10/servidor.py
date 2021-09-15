import socket
import os
from CONSTANTS import *

PORTA = PORTA - 1109

def retorna_info_arquivo(arquivo):
    print(f"\nProcurando arquivo: {arquivo}")
    try:
        arq = arquivo.split(".")
        info_arquivo = {
            "Nome": arq[0]
            , "Extensao": arq[1]
            , "Tamanho": os.stat(f"arquivos//{arquivo}").st_size
        }
        print("Arquivo encontrado")
    except:
        info_arquivo = {
            "Nome": arq[0]
            , "Extensao": arq[1]
            , "Tamanho": 0
        }
        print("Arquivo não encontrado")
    return info_arquivo

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.bind((HOST, PORTA))
tcp.listen()
loop = True
while loop:

    try:
        (socket_cliente, addr) = tcp.accept()
        print("\nConectado a:", socket_cliente)

        print(f"\nEsperando receber conexão {HOST} na porta {PORTA}")
        resposta = False

        msg = socket_cliente.recv(4096)
        msg_info = pickle.loads(msg)
        print(msg_info)


        resposta = retorna_info_arquivo(msg_info[0])

        bytes_resp = pickle.dumps(resposta)

        socket_cliente.send(bytes_resp)

        print("---------------------------------------")

        msg = socket_cliente.recv(4096)
        msg_info = pickle.loads(msg)
        print(msg_info)

        arquivo_upload = f"arquivos//{msg_info[0]}"
        if os.path.isfile(arquivo_upload):
            # Abre o arquivo no modo leitura de bytes
            arquivo_bytes = open(arquivo_upload, 'rb')

            # Envia os dados por partes
            info_bytes = arquivo_bytes.read(1024)
            while info_bytes:
                socket_cliente.send(info_bytes)
                info_bytes = arquivo_bytes.read(1024)

            arquivo_bytes.close()

        else:
            print("Não encontrou o arquivo")
        print("Done")

        if msg == "fim":
            print("\nEncerrando Servidor...")
            tcp.close()

    except Exception as e:
        print(e)
