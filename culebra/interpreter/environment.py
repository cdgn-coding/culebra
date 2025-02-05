from typing import Optional

class Environment:
    def __init__(self, parent: Optional['Environment'] = None):
        self.values: dict[str, any] = {}
        self.parent = parent

    def has(self, name: str):
        if name in self.values:
            return True

        return self.parent and self.parent.has(name)

    def assign_current(self, name: str, value: any):
        self.values[name] = value

    def assign(self, name: str, value: any):
        if name in self.values:
            self.values[name] = value
            return
        elif self.parent and self.parent.has(name):
            self.parent.assign(name, value)
        else:
            self.values[name] = value

    def get(self, name: str) -> any:
        if name in self.values:
            return self.values[name]

        if self.parent and self.parent.has(name):
            return self.parent.get(name)

        raise NameError(f"Undefined variable '{name}'")

    def create_child(self):
        return Environment(self)
