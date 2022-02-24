from pythonosc.udp_client import SimpleUDPClient
from fastapi.websockets import WebSocket
from fastapi import FastAPI
from libs.logger import Logger
from libs.actions import Actions
from libs.tasks import Tasks, RunningTask
from libs.osc_server import OSCServer
import asyncio
from uvicorn import Config, Server
from asyncio import ProactorEventLoop, set_event_loop, ProactorEventLoop, get_event_loop


app = FastAPI()
sender = SimpleUDPClient("127.0.0.1", 9000)
log = Logger()
action = Actions(log)
task = Tasks(log)
oscsrv = OSCServer()

@app.on_event("startup")
async def osc_server():
    asyncio.create_task(oscsrv.start())
    
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
            elif act['action'] == "lk_uw":
                await action.lk_uw(websocket, sender, act)
            elif act['action'] == "lk_dw":
                await action.lk_dw(websocket, sender, act)
            elif act['action'] == "vc_on":
                await action.vc_on(websocket, sender)
            elif act['action'] == "vc_off":
                await action.vc_off(websocket, sender)
            elif act['action'] == "prmt":
                await action.prmt(websocket, sender, act)
            elif act['action'] == "cpu2param_start":
                t = RunningTask()
                t.task_object = await asyncio.create_task(await task.cpu2parameter(websocket, sender, act['parameter']))
                t.websocket = websocket
                await websocket.send_json({"res" : t.id})


if __name__ == "__main__":
    set_event_loop(ProactorEventLoop())
    server = Server(
        config=Config(
            app = app, 
            host = "localhost",
            port = 8000
        )
    )
    get_event_loop().run_until_complete(server.serve())