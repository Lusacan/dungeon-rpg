from dataclasses import dataclass
from typing import Callable

@dataclass
class Action:
    id: int
    description: str
    handler: Callable

    def execute(self):
        return self.handler()