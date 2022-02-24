from pythonosc.osc_server import AsyncIOOSCUDPServer, Dispatcher
import asyncio

def filter_handler(address, *args):
    print(f"{address}: {args}")
    
class OSCServer:

    def __init__(self):
        self.dispatcher = Dispatcher()
        self.dispatcher.map("/avatar/parameters/VRCEmote", filter_handler)
    
    async def loop(self):
        while True:
            print(f"Test")
            await asyncio.sleep(1)

    async def start(self):
        srv = AsyncIOOSCUDPServer(("127.0.0.1", 9001), self.dispatcher, asyncio.get_event_loop())
        transpt, prtc = await srv.create_serve_endpoint()
        
        await self.loop()

        transpt.close()