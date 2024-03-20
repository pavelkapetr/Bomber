import json
def msg(socket, message):
    socket.send(json.dumps(message))
    odpoved = socket.recv()

    print(odpoved)

"""
server: 
    - mapu
    - pozice ostatnich hracu

client:
    - svoji pozici
    - placam bombu ANO/NE
"""