from datetime import datetime
import uuid
from fastapi import status

class ConnectionManager:
    def __init__(self):
        self.ws_clients = []
        self.ws_connections = {}

    def get_ws_clients(self):
        return self.ws_clients
    
    def generateNodeID(self):
        return f"node_{str(uuid.uuid4())}"

    async def send_payload(self, websocket, data):
        await websocket.send_json(data)

    async def create_node(self, websocket):
        node_id = self.generateNodeID()
        websocket.ConnectionTime = int(datetime.now().timestamp())
        websocket.NodeID = node_id
        await websocket.accept()
        self.ws_clients.append(websocket)
        self.ws_connections[websocket.NodeID] = {
            "NodeID" : websocket.NodeID,
            "ConnectionTime" : websocket.ConnectionTime
        }
        
    async def destroy_node(self, websocket, _type):
        if _type == 1000:
            stat = status.WS_1000_NORMAL_CLOSURE
        elif _type == 1005:
            stat = status.WS_1005_ABNORMAL_CLOSURE
        elif _type == 1008:
            stat = status.WS_1008_POLICY_VIOLATION
        await websocket.close(code = stat)
        del self.ws_connections[websocket.NodeID]
        self.ws_clients.remove(websocket)
        