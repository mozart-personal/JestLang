class JestValue:
    pass

class JestFunction(JestValue):
    def __init__(
        self,
        name,
        params,
        body,
        closure
    ):
        self.name = name
        self.params = params
        self.body = body
        self.closure = closure

    def __repr__(self):
        return f"<fn {self.name or 'anonymous'}>"

class NativeFunction(JestValue):
    def __init__(
        self,
        name,
        func
    ):
        self.name = name
        self.func = func

    def __repr__(self):
        return f"<native fn {self.name}>"

class JestObject(JestValue):
    def __init__(self, fields=None):
        self.fields = fields or {}

    def get(self, key):
        return self.fields.get(key)

    def set(self, key, value):
        self.fields[key] = value

    def __getitem__(self, key):
        return self.fields[key]

    def __setitem__(self, key, value):
        self.fields[key] = value

    def __contains__(self, key):
        return key in self.fields

    def __repr__(self):
        return str(self.fields)

class JestArray(JestValue):
    def __init__(self, elements=None):
        self.elements = elements or []

    def push(self, value):
        self.elements.append(value)

    def pop(self):
        return self.elements.pop()

    def get(self, index):
        return self.elements[index]

    def set(self, index, value):
        self.elements[index] = value

    def __getitem__(self, index):
        return self.elements[index]

    def __setitem__(self, index, value):
        self.elements[index] = value

    def __iter__(self):
        return iter(self.elements)

    def __len__(self):
        return len(self.elements)

    def __repr__(self):
        return str(self.elements)