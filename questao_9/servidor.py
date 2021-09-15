import socket
import psutil
from CONSTANTS import *

PORTA = PORTA + 1

def retorna_disco():
    disco = psutil.disk_usage('.')
    percent_uso = round(((disco.used / disco.total) * 100), 2)
    disco_json = {
        "Total": formata_tamanho(disco.total)
        , "Em uso": formata_tamanho(disco.used)
        , "percent_uso": percent_uso
        , "Livre": formata_tamanho(disco.free)
        , "percent_livre": round(100 - percent_uso, 2)
    }
    return disco_json


udp = socket.socket (socket.AF_INET, socket.SOCK_DGRAM)
udp.bind((HOST, PORTA))

while True:
    try:
        print(f"Esperando receber conexão {HOST} na porta {PORTA}")

        (msg, cliente) = udp.recvfrom(1024)
        msg = msg.decode('utf-8')

        if msg == MSG_INICIO:
            resposta = retorna_disco()
            bytes_resp = pickle.dumps(resposta)

            udp.sendto(bytes_resp,cliente)

        while msg == "fim":
            print("Encerrando Servidor...")
            udp.close()

    except Exception as e:
        print(e)
