import json
def msg(socket, message):
    socket.send(json.dumps(message))
    odpoved = socket.recv()
    json

    print(odpoved)
    return odpoved

"""
server: 
    - mapu
    - pozice ostatnich hracu

client:
    - svoji pozici
    - placam bombu ANO/NE
"""