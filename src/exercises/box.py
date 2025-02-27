from dataclasses import dataclass
from typing import List

@dataclass  # Similar to Lombok @Data in Java, but more Pythonic
class Box:
    # Fields with type hints (similar to Java fields with types)
    length: float
    width: float
    height: float
    weight: float
    material: str
    name: str
    number: int

    # In Python, we don't need explicit getters/setters like in Java
    # @dataclass automatically creates __init__, __repr__, __eq__, etc. 