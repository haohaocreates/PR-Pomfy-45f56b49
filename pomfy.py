from server import PromptServer
import torch

def message(id, message):
    if isinstance(message, torch.Tensor):
        string = f"Tensor shape {message.shape}"
    elif isinstance(message, dict) and "samples" in message and isinstance(message["samples"], torch.Tensor):
        string = f"Latent shape {message['samples'].shape}"
    else:
        string = f"{message}"
    PromptServer.instance.send_sync("pomfy-message-handler", {"id": id, "message": string})

class BasePhotoshopOperation():
    CATEGORY = "photoshop"
    FUNCTION = "func"
    INPUT_TYPES = {}
    RETURN_TYPES = {}

class FromPhotoshop(BasePhotoshopOperation):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {"layerName": ("STRING", {"default": ""})},
            "optional": {}
        }
    
    RETURN_NAMES = ("image",)
    RETURN_TYPES = ("IMAGE",)

    def func(self, id, **kwargs):
        for key in kwargs:
            message(id, kwargs[key])
        return ()

class FromPhotoshopMask(BasePhotoshopOperation):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {"layerName": ("STRING", {"default": ""})},
            "optional": {}
        }
    
    RETURN_NAMES = ("mask",)
    RETURN_TYPES = ("MASK",)

    def func(self, id, **kwargs):
        for key in kwargs:
            message(id, kwargs[key])
        return ()

class ToPhotoshop(BasePhotoshopOperation):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {"image": ("IMAGE",)},
            "optional": {
                "layerName": ("STRING", {"default": ""})
            }
        }

    def func(self, id, **kwargs):
        for key in kwargs:
            message(id, kwargs[key])
        return ()
        
class ToPhotoshopMask(BasePhotoshopOperation):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {"mask": ("MASK",)},
            "optional": {
                "layerName": ("STRING", {"default": ""}),
            }
        }

    def func(self, id, **kwargs):
        for key in kwargs:
            message(id, kwargs[key])
        return ()
