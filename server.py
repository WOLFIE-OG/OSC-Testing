from fastapi.websockets import WebSocket, WebSocketDisconnect
from fastapi import FastAPI
from libs.logger import Logger
from libs.actions import Actions
from libs.osc_server import OSCServer
import asyncio
from uvicorn import Config, Server
from asyncio import set_event_loop, get_event_loop
import json


app = FastAPI()
log = Logger()
action = Actions(
    log = log,
    host = "192.168.1.13",
    port = 9000
)
oscsrv = OSCServer(
    log = log,
    host = "localhost",
    port = 9001
)

@app.on_event("startup")
async def osc_server():
    asyncio.create_task(oscsrv.start())

@app.websocket("/ws")
async def websock(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json({"data" : {"type" : "WelcomeMessage", "message" : "Welcome to the websocket"}})
    try:
        while True:
            try:
                _ = await websocket.receive_json()
            except Exception as e:
                if isinstance(e, WebSocketDisconnect) is True:
                    raise WebSocketDisconnect
                else: 
                    await websocket.send_json({"data" : {"type" : "InvalidPayload", "message" : "Welcome to the websocket"}})
                    continue
            _ = await websocket.receive_json()
            if _['type'] == "input_list":
                for act in _['array']:
                    if act['action'] == "prmt":
                        await asyncio.sleep(1)
                    if act['action'] == "jump":
                        await action.jump(websocket)
                    elif act['action'] == "mv_fw":
                        await action.mv_fw(websocket, act)
                    elif act['action'] == "mv_bw":
                        await action.mv_bw(websocket, act)
                    elif act['action'] == "mv_r":
                        await action.mv_r(websocket, act)
                    elif act['action'] == "mv_l":
                        await action.mv_l(websocket, act)
                    elif act['action'] == "lk_l":
                        await action.lk_l(websocket, act)
                    elif act['action'] == "lk_r":
                        await action.lk_r(websocket, act)
                    elif act['action'] == "lk_uw":
                        await action.lk_uw(websocket, act)
                    elif act['action'] == "lk_dw":
                        await action.lk_dw(websocket, act)
                    elif act['action'] == "vc_on":
                        await action.vc_on(websocket)
                    elif act['action'] == "vc_off":
                        await action.vc_off(websocket)
                    elif act['action'] == "prmt":
                        await action.prmt(websocket, act)
            elif _['type'] == "custom_input":
                await action.custom_input(websocket, _)
    except WebSocketDisconnect:
        log.success(f"Websocket Closed, awaiting information")         
    finally:
        await connection_manager.destroy_node(websocket, 1000)
        log.info(f"[-] {websocket.NodeID}")


if __name__ == "__main__":
    #set_event_loop(ProactorEventLoop())
    server = Server(
        config=Config(
            app = app, 
            host = "192.168.1.198",
            port = 8000
        )
    )
    get_event_loop().run_until_complete(server.serve())