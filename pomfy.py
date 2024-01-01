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
    def INPUT_TYPES(cls):  # Use cls as the convention for class methods
        return {"optional": {
            "layerName": ("STRING", {"default": ""}),
            "isMask": ("BOOL", {"default": False})
        }
    }

    RETURN_TYPES = {"image": ("IMAGE",)}

    def func(self, id, **kwargs):
        for key in kwargs:
            message(id, kwargs[key])
        return ()

class ToPhotoshop(BasePhotoshopOperation):
    @classmethod
    def INPUT_TYPES(cls):  # Use cls as the convention for class methods
        return {
            "required": {"image": ("IMAGE",)},
            "optional": {
                "layerName": ("STRING", {"default": ""}),
                "isMask": ("BOOL", {"default": False})
            }
        }

    def func(self, id, **kwargs):
        for key in kwargs:
            message(id, kwargs[key])
        return ()
