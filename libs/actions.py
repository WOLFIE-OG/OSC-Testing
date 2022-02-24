import asyncio
from pythonosc.udp_client import SimpleUDPClient
from fastapi.websockets import WebSocket
from libs.logger import Logger

class Actions:
    def __init__(self, log: Logger):
        self.log = log
        self.sender = SimpleUDPClient("127.0.0.1", 9000)
        self.log.success("Actions Class Initialised")
    
    async def jump(self, websocket: WebSocket):
        await websocket.send_json({"res" : "Jumping"})
        self.sender.send_message("/input/Jump", 1)
        await asyncio.sleep(2)
        self.sender.send_message("/input/Jump", 0)
        self.log.success("Sent jump data")

    async def mv_fw(self, websocket: WebSocket, act: dict):
        await websocket.send_json({"res" : "Moving Forward"})
        if act['is_run'] is True:
            self.sender.send_message("/input/Run", 1)
        self.sender.send_message("/input/MoveForward", 1)
        await asyncio.sleep(act['length'])
        self.sender.send_message("/input/MoveForward", 0)
        self.sender.send_message("/input/Run", 0)
        self.log.success("Sent move forward data")

    async def mv_bw(self, websocket: WebSocket, act: dict):
        await websocket.send_json({"res" : "Moving Backward"})
        if act['is_run'] is True:
            self.sender.send_message("/input/Run", 1)
        self.sender.send_message("/input/MoveBackward", 1)
        await asyncio.sleep(act['length'])
        self.sender.send_message("/input/MoveBackward", 0)
        self.log.success("Sent move backward data")

    async def mv_r(self, websocket: WebSocket, act: dict):
        await websocket.send_json({"res" : "Moving Right"})
        if act['is_run'] is True:
            self.sender.send_message("/input/Run", 1)
        self.sender.send_message("/input/MoveRight", 1)
        await asyncio.sleep(act['length'])
        self.sender.send_message("/input/MoveRight", 0)
        self.log.success("Sent move right data")
    
    async def mv_l(self, websocket: WebSocket, act: dict):
        await websocket.send_json({"res" : "Moving Left"})
        if act['is_run'] is True:
            self.sender.send_message("/input/Run", 1)
        self.sender.send_message("/input/MoveLeft", 1)
        await asyncio.sleep(act['length'])
        self.sender.send_message("/input/MoveLeft", 0)
        self.log.success("Sent move left data")

    async def lk_l(self, websocket: WebSocket, act: dict):
        await websocket.send_json({"res" : "Looking Left"})
        self.sender.send_message("/input/LookLeft", 1)
        await asyncio.sleep(act['length'])
        self.sender.send_message("/input/LookLeft", 0)
        self.log.success("Sent look left data")
    
    async def lk_r(self, websocket: WebSocket, act: dict):
        await websocket.send_json({"res" : "Looking Right"})
        self.sender.send_message("/input/LookRight", 1)
        await asyncio.sleep(act['length'])
        self.sender.send_message("/input/LookRight", 0)
        self.log.success("Sent look right data")
    
    async def lk_uw(self, websocket: WebSocket, act: dict):
        await websocket.send_json({"res" : "Looking Upward"})
        self.sender.send_message("/input/LookUp", 1)
        await asyncio.sleep(act['length'])
        self.sender.send_message("/input/LookUp", 0)
        self.log.success("Sent look upward data")
    
    async def lk_dw(self, websocket: WebSocket, act: dict):
        await websocket.send_json({"res" : "Looking Downward"})
        self.sender.send_message("/input/LookDown", 1)
        await asyncio.sleep(act['length'])
        self.sender.send_message("/input/LookDown", 0)
        self.log.success("Sent look downward data")
    
    async def vc_on(self, websocket: WebSocket):
        await websocket.send_json({"res" : "Turning voice on"})
        self.sender.send_message("/input/Voice", 1)
        self.log.success("Sent voice on data")
    
    async def vc_off(self, websocket: WebSocket):
        await websocket.send_json({"res" : "Turning voice off"})
        self.sender.send_message("/input/Voice", 0)
        self.log.success("Sent voice off data")
    
    async def prmt(self, websocket: WebSocket, act: dict):
        parameter = act['parameter']
        value = act['value']
        await websocket.send_json({"res" : f"Setting {parameter} value too {value}"})
        self.sender.send_message(f"/avatar/parameters/{parameter}", value)
        self.log.success(f"Sent parameter {parameter}:{value} data")
