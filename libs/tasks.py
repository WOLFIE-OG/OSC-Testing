import psutil, asyncio
from pythonosc.udp_client import SimpleUDPClient
from fastapi.websockets import WebSocket
from libs.logger import Logger

class tasks:
    def __init__(self, log: Logger):
        self.log = log

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