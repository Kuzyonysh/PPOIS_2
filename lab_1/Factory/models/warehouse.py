from typing import Union
from .material import Wood, Metal
from .exceptions import InvalidDataError, InvalidAmountError

class Warehouse:
    def __init__(self, name: str, capacity: float):
        self.name = name
        self.capacity = capacity
        self.metal_amount: float = 0.0  
        self.wood_amount: float = 0.0
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str):
        if not value:
            raise InvalidDataError("Name can't be empty")
        self._name = value
    
    @property
    def capacity(self) -> float:
        return self._capacity
    
    @capacity.setter
    def capacity(self, value: float):
        if value is None:
            raise InvalidAmountError("Capacity can't be empty")
        if not isinstance(value, (int, float)):
            raise InvalidAmountError(f"Capacity must be a number, got {type(value).__name__}")
        if value <= 0:
            raise InvalidAmountError("Capacity must be positive")
        self._capacity = float(value)
    
    @property
    def total_amount(self) -> float:
        return self.metal_amount + self.wood_amount
    
    @property
    def available_space(self) -> float:
        return self._capacity - self.total_amount
    
    def add_material(self, material: Union[Metal, Wood]) -> None:
        if not isinstance(material, (Metal, Wood)):
            raise InvalidDataError(f"Expected Metal or Wood, got {type(material).__name__}")
        
        if self.total_amount + material.amount > self._capacity:
            raise InvalidAmountError(
                f"Can't add material. Available: {self.available_space}, "
                f"Required: {material.amount}"
            )
        
        if isinstance(material, Metal):
            self.metal_amount += material.amount
            print(f'Added metal: +{material.amount} (total metal: {self.metal_amount})')
        else:
            self.wood_amount += material.amount
            print(f'Added wood: +{material.amount} (total wood: {self.wood_amount})')
        
        print(f"Warehouse total: {self.total_amount}/{self._capacity} ({self.available_space} free)")
    
    def remove_metal(self, amount: float) -> None:
        if amount > self.metal_amount:
            raise InvalidAmountError(
                f"Not enough metal. Have: {self.metal_amount}, Need: {amount}"
            )
        self.metal_amount -= amount
        print(f"Removed metal: -{amount} (remaining: {self.metal_amount})")
        print(f"Warehouse total: {self.total_amount}/{self._capacity}")
    
    def remove_wood(self, amount: float) -> None:
        if amount > self.wood_amount:
            raise InvalidAmountError(
                f"Not enough wood. Have: {self.wood_amount}, Need: {amount}"
            )
        self.wood_amount -= amount
        print(f"Removed wood: -{amount} (remaining: {self.wood_amount})")
        print(f"Warehouse total: {self.total_amount}/{self._capacity}")
    
    def __str__(self) -> str:
        return (f"Warehouse: {self._name}\n"
                f"Capacity: {self.total_amount}/{self._capacity}\n"
                f"Metal: {self.metal_amount}\n"
                f"Wood: {self.wood_amount}")