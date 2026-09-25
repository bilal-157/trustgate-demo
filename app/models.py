from dataclasses import dataclass

@dataclass
class Product:
    id: int
    name: str
    price: float

@dataclass
class User:
    id: int
    email: str
    password_hash: str
    is_authenticated: bool = False
# clean-03: comment only
