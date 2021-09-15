import json
import pickle

HOST = "127.0.0.1"
PORTA = 9990
MSG_INICIO = "inicio"

def formata_tamanho(byte):
    if byte <= 1024:
        return f"{round(byte, 2)}.00 B"
    elif byte <= 1024**2:
        return f"{round(byte / 1024, 2)} KB"
    elif byte <= 1024**3:
        return f"{round(byte / (1024 * 1024), 2)} MB"
    else:
        return f"{round(byte / (1024 * 1024 * 1024), 2)} GB"