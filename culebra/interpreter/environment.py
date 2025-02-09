from typing import Optional

"""
Culebra Scoping Implementation
=============================

Function-Based Scoping Model:
┌─────────────────────────────────────┐
│ Global Environment                  │
│ ┌─────────────────────────────────┐ │
│ │ Function Environment            │ │
│ │   variables: {...}              │ │
│ │   parent: ↑                     │ │
│ │                                 │ │
│ │   if/while/for blocks           │ │
│ │   share function's scope        │ │
│ └─────────────────────────────────┘ │
│     variables: {...}                │
│     parent: None                    │
└─────────────────────────────────────┘

Variable Resolution:
1. Check current environment
2. If not found, check parent
3. Continue up chain until found or error


Scope Example:
┌────────────────┐  ┌─────────────────────┐
│     Code       │  │      Scopes         │
├────────────────┤  ├─────────────────────┤
│ x = 1          │  │ Global: {x: 1}      │
│ def foo():     │  │   ↓                 │
│   y = 2        │  │ Foo: {y: 2, z: 3}   │
│   if True:     │  │   (blocks share     │
│     z = 3      │  │    function scope)  │
│   return y+z   │  │                     │
└────────────────┘  └─────────────────────┘

Features:
- Function-level scope: New environment only for functions
- Block statements (if/while/for) share their function's scope
- Lexical resolution: Functions retain their definition environment
- Variable shadowing: Inner function scope can hide outer variables
- Dynamic assignment: Can modify outer scope variables
- Closure support: Inner functions capture outer scope
"""

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
