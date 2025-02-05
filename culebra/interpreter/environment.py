from typing import Optional

class Environment:
    def __init__(self, parent: Optional['Environment'] = None):
        self.values: dict[str, any] = {}
        self.parent = parent

    def has(self, name: str):
        if self.parent and self.parent.has(name):
            return True

        return name in self.values

    def assign(self, name: str, value: any):
        if self.parent and self.parent.has(name):
            self.parent.assign(name, value)
        else:
            self.values[name] = value

    def get(self, name: str) -> any:
        if self.parent and self.parent.has(name):
            return self.parent.get(name)

        if name in self.values:
            return self.values[name]
        else:
            raise NameError(f"Undefined variable '{name}'")

    def create_child(self):
        return Environment(self)
