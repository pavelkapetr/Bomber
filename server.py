import asyncio
import websockets
import json
import copy
import time
from Bomba import Bomba1

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
"""
0 = Zeď
1 = Tráva
2 = Box
3 = Tráva (momentálně probíhá výbuch)
4 = Bomba 1
5 = Bomba 2
"""
POCET_HRACU = 2
hra = {"hraci": [], "pripojeni": [i for i in range(POCET_HRACU)], "mapa": copy.deepcopy(mapa), "bomby": [],
       "pozice_hracu": [(1, 1), (7, 1), (1, 7), (7, 7)]}
queue = []


async def handler(websocket):
    global hra
    queue.append(websocket)
    print(f"hraci: {len(queue)} / {POCET_HRACU}")

    if len(queue) >= POCET_HRACU:
        print("zapinam hru")
        for _ in range(POCET_HRACU):
            hra["hraci"].append(queue[0])  # prvniho přesunu
            queue.pop(0)

    while True: # dokud běží, komunikace s clientem je aktivni
        try:
            message = await websocket.recv()
        except Exception as e:
            print("Ztratili jsme ho: ", e)
            try:
                queue.remove(websocket)
            except:
                pass
            if websocket in hra["hraci"]:
                try:
                    hra["pripojeni"].remove(hra["hraci"].index(websocket))
                    if len(hra["pripojeni"]) == 0:
                        hra = {"hraci": [], "pripojeni": POCET_HRACU, "mapa": copy.deepcopy(mapa), "bomby": [],
                               "pozice_hracu": [(1, 1), (7, 1), (1, 7), (7, 7)]}
                except: pass
            break
        # print(message, websocket)
        if message == "info?":
            i = 0
            for hrac in hra["pozice_hracu"]:
                if hrac[0] == 0 and hrac[1] == -2:
                    i += 1
            if i == POCET_HRACU - 1:
                await websocket.send("konec")
                try:
                    hra["pripojeni"].remove(hra["hraci"].index(websocket))
                    if len(hra["pripojeni"]) == 0:
                        hra = {"hraci": [], "pripojeni": POCET_HRACU, "mapa": copy.deepcopy(mapa), "bomby": [],
                               "pozice_hracu": [(1, 1), (7, 1), (1, 7), (7, 7)]}
                except: pass
            else:
                await poslat(websocket)
        elif message == "UŽ?":
            if websocket not in hra["hraci"]:
                await websocket.send("CEKAME")
            else:
                await websocket.send("start")
        else:
            data = json.loads(message)
            index = hra["hraci"].index(websocket)
            hra["pozice_hracu"][index] = data["pozice"]
            if data["bomba"]:
                cas = time.time() * 1000
                Bomb = Bomba1(data["pozice"][0], data["pozice"][1], 1, cas)
                hra["bomby"].append(Bomb)


async def main():
    async with websockets.serve(handler, "", 8000):
        await asyncio.Future()  # run forever


async def poslat(socket):
    if len(hra["bomby"]) > 0:
        mapa = copy.deepcopy(hra["mapa"])
        for bomb in hra["bomby"]:
            x, y = bomb.pole_x, bomb.pole_y
            i = bomb.fajci(mapa)
            if i == 4 or i == 5:
                mapa[x][y] = i
            else:
                hra["mapa"] = mapa
            if bomb.smrt:
                hra["bomby"].remove(bomb)
        await socket.send(json.dumps(
            {
                "mapa": mapa,
                "pozice_hracu": hra["pozice_hracu"],
                "index_hrace": hra["hraci"].index(socket)
            }
        ))
    else:
        await socket.send(json.dumps(
            {
                "mapa": hra["mapa"],
                "pozice_hracu": hra["pozice_hracu"],
                "index_hrace": hra["hraci"].index(socket)
            }
        ))


if __name__ == "__main__":
    print("ZAPINAM SERVER")
    asyncio.run(main())
