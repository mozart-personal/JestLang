from flask import Flask, jsonify, request
import threading
from runtime.values import NativeFunction, JestObject

class WebModule:
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.app = Flask("Jestlang")
        self.routes = []
        
        self.fields = {
            "get": NativeFunction("get", self.get),
            "post": NativeFunction("post", self.post),
            "run": NativeFunction("run", self.run)
        }

    def get(self, path, handler=None):
        if handler is None:
            def decorator(h):
                self.add_route(path, h, ["GET"])
                return h
            return NativeFunction("get_dec", decorator)
        self.add_route(path, handler, ["GET"])

    def post(self, path, handler=None):
        if handler is None:
            def decorator(h):
                self.add_route(path, h, ["POST"])
                return h
            return NativeFunction("post_dec", decorator)
        self.add_route(path, handler, ["POST"])

    def add_route(self, path, handler, methods):
        flask_path = path.replace("/:", "/<").replace(":", ">")
        
        def flask_handler(**kwargs):
            self.interpreter.globals["params"] = kwargs
            result = self.interpreter.call_function(handler, [])
            if isinstance(result, dict):
                return jsonify(result)
            if hasattr(result, "fields"):
                return jsonify(result.fields)
            return jsonify(result)

        self.app.add_url_rule(flask_path, f"route_{path}_{methods[0]}", flask_handler, methods=methods)

    def run(self, port):
        print(f"Jestlang Web Server running on port {port}...")
        
        self.app.run(port=int(port), debug=False, use_reloader=False)

    def __repr__(self):
        return "<module web>"
