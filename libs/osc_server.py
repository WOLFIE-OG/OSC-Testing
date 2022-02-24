from pythonosc.osc_server import AsyncIOOSCUDPServer, Dispatcher
import asyncio
from libs.logger import Logger

def vrc_emote_handler(address, *args):
    print(f"{address}: {args}")

class OSCServer:

    def __init__(self, log: Logger):
        self.log = log
        self.is_open = False
        self.dispatcher = Dispatcher()
        self.dispatcher.map("/avatar/parameters/VRCEmote", vrc_emote_handler)
        self.log.success("OSCServer Class Initialised")
    
    async def loop(self):
        while self.is_open is not False:
            pass
            await asyncio.sleep(1)
        self.stop()

    async def start(self):
        srv = AsyncIOOSCUDPServer(("127.0.0.1", 9001), self.dispatcher, asyncio.get_event_loop())
        self.transpt, prtc = await srv.create_serve_endpoint()
        self.is_open = True
        await self.loop()
    
    async def stop(self):
        self.transpt.close()