import asyncio
import websockets
import json
import copy

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
hra = {"hraci": [], "mapa": copy.deepcopy(mapa), "bomby": [], "pozice_hracu": [(1, 1), (7, 1), (1, 7), (7, 7)]}
queue = []
POCET_HRACU = 2
START_POS= []

async def handler(websocket):
    queue.append(websocket)
    print(f"hraci: {len(queue)} / {POCET_HRACU}")

    if len(queue) >= POCET_HRACU:
        print("zapinam hru")
        for _ in range(POCET_HRACU):
            hra["hraci"].append(queue[0]) # prvniho přesunu
            queue.pop(0)

    while True: # dokud běží, komunikace s clientem je aktivni
        try:
            message = await websocket.recv() # pockám na request ale nezajímá mě co poslal
        except Exception as e:
            print("Ztratili jsme ho: ", e)
            queue.remove(websocket)
            break
        if websocket in hra["hraci"]:
            await poslat(websocket)
        else:
            await websocket.send("CEKAME")
        print(message, websocket)
        if message == "info?":
            await poslat(websocket)
            print("posláno", websocket)

async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever

async def poslat(socket):
    await socket.send(json.dumps(
        {
            "mapa": hra["mapa"],
            "bomby": hra["bomby"],
            "pozice_hracu": hra["pozice_hracu"],
            "index_hrace": hra["hraci"].index(socket)
        }
    ))

if __name__ == "__main__":
    print("ZAPINAM SERVER")
    asyncio.run(main())