from server import PromptServer
import torch
import base64
import json
import asyncio

class BasePhotoshopOperation():
    CATEGORY = "photoshop"
    FUNCTION = "func"
    INPUT_TYPES = {}
    RETURN_TYPES = {}

class BaseWebSocketListener:
    async def websocket_listener(self, ws, layerName, dataType):
        try:
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    data = json.loads(msg.data)
                    if dataType in data and "layerName" in data and data["layerName"] == layerName:
                        decoded_data = data[dataType]
                        return base64.b64decode(decoded_data)
        except Exception as e:
            print(f'WebSocket listener error: {e}')
        return None

class FromPhotoshop(BasePhotoshopOperation, BaseWebSocketListener):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {"layerName": ("STRING", {"default": ""})},
            "optional": {}
        }

    RETURN_NAMES = ("image",)
    RETURN_TYPES = ("IMAGE",)

    def func(self, layerName):
        image_data = asyncio.run(self.websocket_listener(
            PromptServer.instance.sockets[self.client_id], layerName, "image"
        ))
        return (image_data,)

class FromPhotoshopMask(BasePhotoshopOperation, BaseWebSocketListener):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {"layerName": ("STRING", {"default": ""})},
            "optional": {}
        }

    RETURN_NAMES = ("mask",)
    RETURN_TYPES = ("MASK",)

    def func(self, layerName):
        mask_data = asyncio.run(self.websocket_listener(
            PromptServer.instance.sockets[self.client_id], layerName, "mask"
        ))
        return  (mask_data,)


class ToPhotoshop(BasePhotoshopOperation):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {"image": ("IMAGE",)},
            "optional": {"layerName": ("STRING", {"default": ""})}
        }

    OUTPUT_NODE = True

    def func(self, image, layerName):
        image_data = ("PNG", image)
        PromptServer.instance.send(BinaryEventTypes.UNENCODED_PREVIEW_IMAGE, image_data)
        return ()

class ToPhotoshopMask(BasePhotoshopOperation):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {"mask": ("MASK",)},
            "optional": {"layerName": ("STRING", {"default": ""})}
        }

    OUTPUT_NODE = True

    def func(self, mask, layerName):
        mask_data = ("PNG", mask)
        PromptServer.instance.send_sync("image", mask_data)
        return ()