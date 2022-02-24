import psutil, asyncio
from pythonosc.udp_client import SimpleUDPClient
from fastapi.websockets import WebSocket
from libs.logger import Logger
from uuid import uuid4

class RunningTask:
    task_object: any
    websocket: WebSocket
    id: str = str(uuid4())

class Tasks:
    def __init__(self, log: Logger):
        self.log = log
        self.tasks = []

    async def cpu2parameter(self, websocket: WebSocket, sender: SimpleUDPClient, parameter: str):
        while True:
            cpu = psutil.cpu_percent() / 350
            if cpu != 0.0:
                self.log.info(cpu)
                sender.send_message(
                    address = f"/avatar/parameters/{parameter}",
                    value = float(cpu)
                )
                await websocket.send_json({"res" : f"Sent CPU {cpu}"})