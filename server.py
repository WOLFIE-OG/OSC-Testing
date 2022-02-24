from pythonosc.udp_client import SimpleUDPClient
from fastapi.websockets import WebSocket
from fastapi import FastAPI
import uvicorn, asyncio

app = FastAPI()
sender = SimpleUDPClient("127.0.0.1", 9000)

@app.websocket("/ws")
async def websock(websocket: WebSocket):
    await websocket.accept()
    while True:
        
        _ = await websocket.receive_json()
        for act in _['array']:
            if act['action'] == "jump":
                await websocket.send_json({"res" : "Jumping"})
                sender.send_message("/input/Jump", 1)
                await asyncio.sleep(0.3)
                sender.send_message("/input/Jump", 0)
            
            elif act['action'] == "mv_fw":
                await websocket.send_json({"res" : "Moving Forward"})
                if act['isRun'] is True:
                    sender.send_message("/input/Run", 1)
                sender.send_message("/input/MoveForward", 1)
                await asyncio.sleep(act['length'])
                sender.send_message("/input/MoveForward", 0)
                sender.send_message("/input/Run", 0)
            
            elif act['action'] == "mv_bw":
                await websocket.send_json({"res" : "Moving Backward"})
                if act['isRun'] is True:
                    sender.send_message("/input/Run", 1)
                sender.send_message("/input/MoveBackward", 1)
                await asyncio.sleep(act['length'])
                sender.send_message("/input/MoveBackward", 0)
            
            elif act['action'] == "mv_r":
                await websocket.send_json({"res" : "Moving Right"})
                if act['isRun'] is True:
                    sender.send_message("/input/Run", 1)
                sender.send_message("/input/MoveRight", 1)
                await asyncio.sleep(act['length'])
                sender.send_message("/input/MoveRight", 0)
            
            elif act['action'] == "mv_l":
                await websocket.send_json({"res" : "Moving Left"})
                if act['isRun'] is True:
                    sender.send_message("/input/Run", 1)
                sender.send_message("/input/MoveLeft", 1)
                await asyncio.sleep(act['length'])
                sender.send_message("/input/MoveLeft", 0)
            
            elif act['action'] == "lk_l":
                await websocket.send_json({"res" : "Looking Left"})
                sender.send_message("/input/LookLeft", 1)
                await asyncio.sleep(act['length'])
                sender.send_message("/input/LookLeft", 0)
            
            elif act['action'] == "lk_r":
                await websocket.send_json({"res" : "Looking Right"})
                sender.send_message("/input/LookRight", 1)
                await asyncio.sleep(act['length'])
                sender.send_message("/input/LookRight", 0)
            
            elif act['action'] == "vc_on":
                await websocket.send_json({"res" : "Turning voice on"})
                sender.send_message("/input/Voice", 1)
            
            elif act['action'] == "vc_off":
                await websocket.send_json({"res" : "Turning voice off"})
                sender.send_message("/input/Voice", 0)
 
        
uvicorn.run(app)