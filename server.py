from pythonosc.udp_client import SimpleUDPClient
from fastapi.websockets import WebSocket
from fastapi import FastAPI
from libs.logger import Logger
from libs.actions import actions
from libs.tasks import tasks
import uvicorn, asyncio

app = FastAPI()
sender = SimpleUDPClient("127.0.0.1", 9000)
log = Logger()
action = actions(log)
task = tasks(log)

@app.websocket("/ws")
async def websock(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("WELCOME TO SOME SHITTY THING I MADE, PLEASE DONT BREAK MY SHIT")
    while True:
        _ = await websocket.receive_json()
        for act in _['array']:
            if act['action'] == "prmt":
                await asyncio.sleep(1)
            if act['action'] == "jump":
                await action.jump(websocket, sender)
            elif act['action'] == "mv_fw":
                await action.mv_fw(websocket, sender, act)
            elif act['action'] == "mv_bw":
                await action.mv_bw(websocket, sender, act)
            elif act['action'] == "mv_r":
                await action.mv_r(websocket, sender, act)
            elif act['action'] == "mv_l":
                await action.mv_l(websocket, sender, act)
            elif act['action'] == "lk_l":
                await action.lk_l(websocket, sender, act)
            elif act['action'] == "lk_r":
                await action.lk_r(websocket, sender, act)
            elif act['action'] == "vc_on":
                await action.vc_on(websocket, sender)
            elif act['action'] == "vc_off":
                await action.vc_off(websocket, sender)
            elif act['action'] == "prmt":
                await action.prmt(websocket, sender, act)
            elif act['action'] == "cpu2param":
                asyncio.create_task(task.cpu2parameter(websocket, sender, act['parameter']))
uvicorn.run(app)