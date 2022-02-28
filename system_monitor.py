import asyncio
import aiohttp
import json
import psutil
import platform
import base64
import GPUtil

from colorama import init, Fore
import datetime
import pathlib

class Logger:
    def __init__(self):
        """Logging module"""
        init()
    
    def info(self, info):
        """Out put info message"""
        print(f"{Fore.BLUE}INFO{Fore.WHITE}:     {info}")
    
    def success(self, success):
        """Out put success message"""
        print(f"{Fore.GREEN}SUCCESS{Fore.WHITE}:  {success}")

    def error(self, error):
        """Out put error message"""
        print(f"{Fore.RED}ERROR{Fore.WHITE}:    {error}")

    def warning(self, warning):
        """Out put warning message"""
        print(f"{Fore.YELLOW}WARNING{Fore.WHITE}:  {warning}")

class Node:
    def __init__(self, url):
        self.url = url
        self.log = Logger()
    
    async def sendUsage(self, node):
        while True:
            cpu = psutil.cpu_percent() / 100
            ram = psutil.virtual_memory().percent / 100
            gpu_l = GPUtil.getGPUs()
            gpu = gpu_l[0].load*100 / 100 if len(gpu_l) != 0 else 0.0
            self.log.info(f"CPU: {cpu} | RAM: {ram} | GPU: {gpu}")
            await node.send_json(
                {
                    "type" : "custom_input",
                    "custom_data" : {
                        "cpu" : {
                            "address" : "/avatar/parameters/CPUF",
                            "value" : float(cpu)
                        },
                        "ram" : {
                            "address" : "/avatar/parameters/RAMF",
                            "value" : float(ram)
                        },
                        "gpu" : {
                            "address" : "/avatar/parameters/GPUF",
                            "value" : float(gpu)
                        },
                    }
                }
            )
            await asyncio.sleep(0.1)
    
    async def start(self):
        while True:
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.ws_connect(self.url, max_msg_size=80000000) as ws:
                        asyncio.create_task(self.sendUsage(ws))
                        while True:
                            _ = await ws.receive_json()
                            pass
            
                
                except Exception as e:
                    if isinstance(e, TypeError):
                        pass
                    else:
                        self.log.error(e)

node = Node("ws://192.168.1.198:8000/ws")
asyncio.get_event_loop().run_until_complete(node.start())