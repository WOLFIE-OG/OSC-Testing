import asyncio
from pythonosc.udp_client import SimpleUDPClient
from fastapi.websockets import WebSocket
from libs.logger import Logger
from libs.payloads import Payloads

class Actions:
    def __init__(self, log: Logger, host: str, port: int):
        self.log = log
        self.sender = SimpleUDPClient(host, port)
        self.log.success("Actions Class Initialised")
    
    async def custom_input(self, websocket: WebSocket, _):
        await websocket.send_json(Payloads.payload(
            self,
            type = "custom_input_sent",
            message = "Sent Custom Input"
        ))
        for name in dict(_['custom_data']).keys():
            self.sender.send_message(_['custom_data'][name]['address'], _['custom_data'][name]['value'])
            self.log.success(f"Sent Custom Input {_['custom_data'][name]['address']}:{_['custom_data'][name]['value']}")

    async def jump(self, websocket: WebSocket):
        await websocket.send_json(Payloads.payload(
            self,
            type = "input_sent",
            message = "Sent Jump Input"
        ))
        self.sender.send_message("/input/Jump", 1)
        await asyncio.sleep(2)
        self.sender.send_message("/input/Jump", 0)
        self.log.success("Sent Jump Input")

    async def mv_fw(self, websocket: WebSocket, act: dict):
        await websocket.send_json(Payloads.payload(
            self,
            type = "input_sent",
            message = "Sent Move Forward Input"
        ))
        if act['is_run'] is True:
            self.sender.send_message("/input/Run", 1)
        self.sender.send_message("/input/MoveForward", 1)
        await asyncio.sleep(act['length'])
        self.sender.send_message("/input/MoveForward", 0)
        self.sender.send_message("/input/Run", 0)
        self.log.success("Sent Move Forward Input")

    async def mv_bw(self, websocket: WebSocket, act: dict):
        await websocket.send_json(Payloads.payload(
            self,
            type = "input_sent",
            message = "Sent Move Backward Input"
        ))
        if act['is_run'] is True:
            self.sender.send_message("/input/Run", 1)
        self.sender.send_message("/input/MoveBackward", 1)
        await asyncio.sleep(act['length'])
        self.sender.send_message("/input/MoveBackward", 0)
        self.log.success("ent Move Backward Input")

    async def mv_r(self, websocket: WebSocket, act: dict):
        await websocket.send_json(Payloads.payload(
            self,
            type = "input_sent",
            message = "Sent Move Right Input"
        ))
        if act['is_run'] is True:
            self.sender.send_message("/input/Run", 1)
        self.sender.send_message("/input/MoveRight", 1)
        await asyncio.sleep(act['length'])
        self.sender.send_message("/input/MoveRight", 0)
        self.log.success("Sent Move Right Input")
    
    async def mv_l(self, websocket: WebSocket, act: dict):
        await websocket.send_json(Payloads.payload(
            self,
            type = "input_sent",
            message = "Sent Move Left Input"
        ))
        if act['is_run'] is True:
            self.sender.send_message("/input/Run", 1)
        self.sender.send_message("/input/MoveLeft", 1)
        await asyncio.sleep(act['length'])
        self.sender.send_message("/input/MoveLeft", 0)
        self.log.success("Sent Move Left Input")

    async def lk_l(self, websocket: WebSocket, act: dict):
        await websocket.send_json(Payloads.payload(
            self,
            type = "input_sent",
            message = "Sent Look Left Input"
        ))
        self.sender.send_message("/input/LookLeft", 1)
        await asyncio.sleep(act['length'])
        self.sender.send_message("/input/LookLeft", 0)
        self.log.success("Sent Look Left Input")
    
    async def lk_r(self, websocket: WebSocket, act: dict):
        await websocket.send_json(Payloads.payload(
            self,
            type = "input_sent",
            message = "Sent Look Right Input"
        ))
        self.sender.send_message("/input/LookRight", 1)
        await asyncio.sleep(act['length'])
        self.sender.send_message("/input/LookRight", 0)
        self.log.success("Sent Look Right Input")
    
    async def lk_uw(self, websocket: WebSocket, act: dict):
        await websocket.send_json(Payloads.payload(
            self,
            type = "input_sent",
            message = "Sent Look Up Input"
        ))
        self.sender.send_message("/input/LookUp", 1)
        await asyncio.sleep(act['length'])
        self.sender.send_message("/input/LookUp", 0)
        self.log.success("Sent Look Up Input")
    
    async def lk_dw(self, websocket: WebSocket, act: dict):
        await websocket.send_json(Payloads.payload(
            self,
            type = "input_sent",
            message = "Sent Look Down Input"
        ))
        self.sender.send_message("/input/LookDown", 1)
        await asyncio.sleep(act['length'])
        self.sender.send_message("/input/LookDown", 0)
        self.log.success("Sent Look Down Input")
    
    async def vc_on(self, websocket: WebSocket):
        await websocket.send_json(Payloads.payload(
            self,
            type = "input_sent",
            message = "Sent Voice On Input"
        ))
        self.sender.send_message("/input/Voice", 1)
        self.log.success("Sent Voice On Input")
    
    async def vc_off(self, websocket: WebSocket):
        await websocket.send_json(Payloads.payload(
            self,
            type = "input_sent",
            message = "Sent Voice Off Input"
        ))
        self.sender.send_message("/input/Voice", 0)
        self.log.success("Sent Voice Off Input")
    
    async def prmt(self, websocket: WebSocket, act: dict):
        parameter = act['parameter']
        value = act['value']
        await websocket.send_json(Payloads.payload(
            self,
            type = "input_sent",
            message = f"Setting {parameter} value too {value}"
        ))
        self.sender.send_message(f"/avatar/parameters/{parameter}", value)
        self.log.success(f"Setting {parameter} value too {value}")
