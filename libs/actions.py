import asyncio
from pythonosc.udp_client import SimpleUDPClient
from fastapi.websockets import WebSocket
from libs.logger import Logger

class actions:
    def __init__(self, log: Logger):
        self.log = log
    
    async def jump(self, websocket: WebSocket, sender: SimpleUDPClient):
        await websocket.send_json({"res" : "Jumping"})
        sender.send_message("/input/Jump", 1)
        await asyncio.sleep(0.3)
        sender.send_message("/input/Jump", 0)
        self.log.success("Sent jump data")

    async def mv_fw(self, websocket: WebSocket, sender: SimpleUDPClient, act: dict):
        await websocket.send_json({"res" : "Moving Forward"})
        if act['is_run'] is True:
            sender.send_message("/input/Run", 1)
        sender.send_message("/input/MoveForward", 1)
        await asyncio.sleep(act['length'])
        sender.send_message("/input/MoveForward", 0)
        sender.send_message("/input/Run", 0)
        self.log.success("Sent move forward data")

    async def mv_bw(self, websocket: WebSocket, sender: SimpleUDPClient, act: dict):
        await websocket.send_json({"res" : "Moving Backward"})
        if act['is_run'] is True:
            sender.send_message("/input/Run", 1)
        sender.send_message("/input/MoveBackward", 1)
        await asyncio.sleep(act['length'])
        sender.send_message("/input/MoveBackward", 0)
        self.log.success("Sent move backward data")

    async def mv_r(self, websocket: WebSocket, sender: SimpleUDPClient, act: dict):
        await websocket.send_json({"res" : "Moving Right"})
        if act['is_run'] is True:
            sender.send_message("/input/Run", 1)
        sender.send_message("/input/MoveRight", 1)
        await asyncio.sleep(act['length'])
        sender.send_message("/input/MoveRight", 0)
        self.log.success("Sent move right data")
    
    async def mv_l(self, websocket: WebSocket, sender: SimpleUDPClient, act: dict):
        await websocket.send_json({"res" : "Moving Left"})
        if act['is_run'] is True:
            sender.send_message("/input/Run", 1)
        sender.send_message("/input/MoveLeft", 1)
        await asyncio.sleep(act['length'])
        sender.send_message("/input/MoveLeft", 0)
        self.log.success("Sent move left data")

    async def lk_l(self, websocket: WebSocket, sender: SimpleUDPClient, act: dict):
        await websocket.send_json({"res" : "Looking Left"})
        sender.send_message("/input/LookLeft", 1)
        await asyncio.sleep(act['length'])
        sender.send_message("/input/LookLeft", 0)
        self.log.success("Sent look left data")
    
    async def lk_r(self, websocket: WebSocket, sender: SimpleUDPClient, act: dict):
        await websocket.send_json({"res" : "Looking Right"})
        sender.send_message("/input/LookRight", 1)
        await asyncio.sleep(act['length'])
        sender.send_message("/input/LookRight", 0)
        self.log.success("Sent look right data")
    
    async def vc_on(self, websocket: WebSocket, sender: SimpleUDPClient):
        await websocket.send_json({"res" : "Turning voice on"})
        sender.send_message("/input/Voice", 1)
        self.log.success("Sent voice on data")
    
    async def vc_off(self, websocket: WebSocket, sender: SimpleUDPClient):
        await websocket.send_json({"res" : "Turning voice off"})
        sender.send_message("/input/Voice", 0)
        self.log.success("Sent voice off data")
    
    async def prmt(self, websocket: WebSocket, sender: SimpleUDPClient, act: dict):
        parameter = act['parameter']
        value = act['value']
        await websocket.send_json({"res" : f"Setting {parameter} value too {value}"})
        sender.send_message(f"/avatar/parameters/{parameter}", value)
        self.log.success(f"Sent parameter {parameter}:{value} data")