import socket
from CONSTANTS import *

PORTA = PORTA + 1

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest = (HOST, PORTA)
print(f"Realizando conexão {HOST} na porta {PORTA}")
msg = MSG_INICIO
udp.sendto(msg.encode("utf-8"),dest)

(resposta,servidor) = udp.recvfrom(4096)

udp.close()

disco_json = pickle.loads(resposta, fix_imports=True, encoding="utf-8")
print(json.dumps(disco_json, indent=4, sort_keys=True))

