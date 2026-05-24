class JestValue:
    pass

class JestFunction(JestValue):
    def __init__(self, name, params, body, closure):
        self.name = name
        self.params = params
        self.body = body
        self.closure = closure

    def __repr__(self):
        return f"<fn {self.name or 'anonymous'}>"

class NativeFunction(JestValue):
    def __init__(self, name, func):
        self.name = name
        self.func = func

    def __repr__(self):
        return f"<native fn {self.name}>"

class JestObject(JestValue):
    def __init__(self, fields=None):
        self.fields = fields or {}

    def __repr__(self):
        return str(self.fields)

class JestArray(JestValue):
    def __init__(self, elements=None):
        self.elements = elements or []

    def __repr__(self):
        return str(self.elements)
