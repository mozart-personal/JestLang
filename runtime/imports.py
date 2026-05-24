import importlib.util
import os
import sys

class ImportSystem:
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.loaded_cogs = {}

    def load(self, module_name):
        if module_name in self.loaded_cogs:
            return self.loaded_cogs[module_name]

        if module_name == "web":
            from runtime.web import WebModule
            cog = WebModule(self.interpreter)
            self.loaded_cogs[module_name] = cog
            return cog

        raise Exception(f"Module '{module_name}' not found")
