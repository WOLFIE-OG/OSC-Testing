from pythonosc.osc_server import AsyncIOOSCUDPServer, Dispatcher
import asyncio
from libs.logger import Logger

def vrc_emote_handler(address, *args):
    print(f"{address}: {args}")

class OSCServer:
    def __init__(self, log: Logger, host: str, port: int):
        self.log = log
        self.is_open = False
        self.dispatcher = Dispatcher()
        self.dispatcher.map("/avatar/parameters/VRCEmote", vrc_emote_handler)
        self.server = AsyncIOOSCUDPServer((host, port), self.dispatcher, asyncio.get_event_loop())
        self.log.success("OSCServer Class Initialised")
    
    async def loop(self):
        while self.is_open is not False:
            pass
            await asyncio.sleep(1)
        self.stop()

    async def start(self):
        self.transpt, prtc = await self.server.create_serve_endpoint()
        self.is_open = True
        await self.loop()
    
    async def stop(self):
        self.transpt.close()