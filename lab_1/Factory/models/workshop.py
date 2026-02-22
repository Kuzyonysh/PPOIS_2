from .furniture import Furniture
from typing import List
from .exceptions import InvalidDataError

class Workshop:
    def __init__(self, workshop_type: str):
        self.workshop_type = workshop_type
        self.completed_furnitures: List[Furniture] = []
    
    @property
    def workshop_type(self) -> str:
        return self._workshop_type
    
    @workshop_type.setter
    def workshop_type(self, value: str):
        if not value:
            raise InvalidDataError("Workshop type can't be empty")
        self._workshop_type = value
    
    def add_completed_furniture(self, furniture: Furniture) -> None:
        self.completed_furnitures.append(furniture)
        print(f"Added {furniture.type} to {self._workshop_type} workshop storage")
    
    def get_completed_count(self) -> int:
        return len(self.completed_furnitures)
    
    def get_completed_list(self) -> List[str]:
        return [f.type for f in self.completed_furnitures]
    
    def __str__(self) -> str:
        return (f"Workshop: {self._workshop_type}\n"
                f"Completed furniture: {len(self.completed_furnitures)}")