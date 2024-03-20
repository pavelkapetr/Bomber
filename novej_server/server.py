import asyncio
import websockets
import json

queue = set()
hra = {}

mapa = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 2, 2, 2, 1, 1, 0],
    [0, 1, 0, 2, 0, 2, 0, 1, 0],
    [0, 2, 2, 2, 2, 2, 2, 2, 0],
    [0, 2, 0, 2, 0, 2, 0, 2, 0],
    [0, 2, 2, 2, 2, 2, 2, 2, 0],
    [0, 1, 0, 2, 0, 2, 0, 1, 0],
    [0, 1, 1, 2, 2, 2, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]

async def server(websocket):
    global hra, queue
    print("pripojil se")
    queue.add(websocket)
    try:
        async for message in websocket:
            if len(queue) >= 2:
                hra = {"hraci": [], "mapa": mapa.copy(), "bomby": []}
                hraci = list(queue)
                for i in range(2):
                    hra["hraci"].append((hraci[i], 0, 0))

                for h in hra["hraci"]:
                    await h[0].send("ZACINAME")

                queue = set()

            elif message == "UŽ?":
                await websocket.send("NE")

            else: # už hrajeme
                # pozmenit mapu a poslat info zpatky
                print(message)
                await websocket.send(json.dumps(hra["mapa"]))

    except Exception as e:
        print("ztratili jsme ho", e)
        if websocket in queue:
            queue.remove(websocket)


print("start server")

start = websockets.serve(server, "localhost", 8000)

asyncio.get_event_loop().run_until_complete(start)
asyncio.get_event_loop().run_forever()