from flask import Flask
from flask import jsonify
from flask import request

from runtime.values import (
    NativeFunction,
    JestObject,
    JestArray
)

class WebModule:
    def __init__(self, interpreter):
        self.interpreter = interpreter

        self.app = Flask("Jestlang")

        self.fields = {
            "get": NativeFunction(
                "get",
                self.get
            ),

            "post": NativeFunction(
                "post",
                self.post
            ),

            "put": NativeFunction(
                "put",
                self.put
            ),

            "delete": NativeFunction(
                "delete",
                self.delete
            ),

            "run": NativeFunction(
                "run",
                self.run
            )
        }

    def convert_path(self, path):
        parts = path.split("/")

        converted = []

        for part in parts:
            if part.startswith(":"):
                converted.append(
                    f"<{part[1:]}>"
                )
            else:
                converted.append(part)

        return "/".join(converted)

    def register_route(
        self,
        method,
        path,
        handler
    ):
        flask_path = self.convert_path(path)

        endpoint_name = (
            f"{method}_{path}"
            .replace("/", "_")
            .replace("<", "")
            .replace(">", "")
            .replace(":", "")
        )

        def endpoint(**kwargs):
            params = JestObject(kwargs)

            self.interpreter.globals.define(
                "params",
                params
            )

            body = request.get_json(
                silent=True
            ) or {}

            self.interpreter.globals.define(
                "body",
                JestObject(body)
            )

            query = JestObject(
                request.args.to_dict()
            )

            self.interpreter.globals.define(
                "query",
                query
            )

            headers = JestObject(
                dict(request.headers)
            )

            self.interpreter.globals.define(
                "headers",
                headers
            )

            result = self.interpreter.call_function(
                handler,
                []
            )

            return self.serialize(result)

        self.app.add_url_rule(
            flask_path,
            endpoint_name,
            endpoint,
            methods=[method]
        )

    def get(self, path, handler):
        self.register_route(
            "GET",
            path,
            handler
        )

    def post(self, path, handler):
        self.register_route(
            "POST",
            path,
            handler
        )

    def put(self, path, handler):
        self.register_route(
            "PUT",
            path,
            handler
        )

    def delete(self, path, handler):
        self.register_route(
            "DELETE",
            path,
            handler
        )

    def serialize(self, value):
        if isinstance(value, JestObject):
            return jsonify(
                self.normalize(value.fields)
            )

        if isinstance(value, JestArray):
            return jsonify(
                self.normalize(value.elements)
            )

        return jsonify(
            self.normalize(value)
        )

    def normalize(self, value):
        if isinstance(value, JestObject):
            return {
                key: self.normalize(val)
                for key, val in value.fields.items()
            }

        if isinstance(value, JestArray):
            return [
                self.normalize(item)
                for item in value.elements
            ]

        if isinstance(value, dict):
            return {
                key: self.normalize(val)
                for key, val in value.items()
            }

        if isinstance(value, list):
            return [
                self.normalize(item)
                for item in value
            ]

        return value

    def run(self, port=3000):
        print(
            f"Jestlang server running on http://localhost:{port}"
        )

        self.app.run(
            host="0.0.0.0",
            port=int(port),
            debug=False,
            use_reloader=False
        )

    def __repr__(self):
        return "<module web>"