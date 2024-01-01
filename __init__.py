import os
from .photoshop import FromPhotoshop, ToPhotoshop

POMFY_VERSION = "0.1.0"

NODE_CLASS_MAPPINGS = {}  # Define the dictionary here

NODE_CLASS_MAPPINGS["To Photoshop"] = ToPhotoshop
NODE_CLASS_MAPPINGS["From Photoshop"] = FromPhotoshop

WEB_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)), "js")
__all__ = ['NODE_CLASS_MAPPINGS', "WEB_DIRECTORY"]