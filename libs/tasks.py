import psutil, asyncio, GPUtil
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
        self.sender = SimpleUDPClient("127.0.0.1", 9000)

    async def system2parameter(self, websocket: WebSocket):
        gpu_l = GPUtil.getGPUs()
        while True:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            gpu = gpu_l[0].load*100
            self.log.info(f"CPU: {cpu} | RAM: {ram} | GPU: {gpu}")
            self.sender.send_message(
                address = f"/avatar/parameters/CPUF",
                value = float(cpu)
            )
            self.sender.send_message(
                address = f"/avatar/parameters/RAMF",
                value = float(ram)
            )
            self.sender.send_message(
                address = f"/avatar/parameters/GPUF",
                value = float(gpu)
            )
            await websocket.send_json({"res" : f"CPU: {cpu} | RAM: {ram} | GPU: {gpu}"})
            await asyncio.sleep(0.1)