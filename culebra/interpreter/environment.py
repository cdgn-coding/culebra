

class Environment:
    def __init__(self):
        self.values: dict[str, any] = {}

    def has(self, name: str):
        return name in self.values

    def assign(self, name: str, value: any):
        self.values[name] = value

    def get(self, name: str) -> any:
        if name in self.values:
            return self.values[name]
        else:
            raise NameError(f"Undefined variable '{name}'")
