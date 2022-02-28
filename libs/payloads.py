
class Payloads:
    
    def payload(self, type: str, message: str, custom_data: list = None):
        payload = {
            "data" : {
                "type" : type,
                "message" : message,
                "custom_data" : custom_data
            }
        }
        return payload