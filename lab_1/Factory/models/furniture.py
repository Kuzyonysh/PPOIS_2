from enum import Enum
from typing import List
from .material import Material
from .exceptions import InvalidDataError

class FurnitureState(Enum):
    CREATED = "Created"
    MATERIALS_PREPARED = "Materials Prepared"
    ELEMENTS_MANUFACTURED = "Elements Manufactured"
    ASSEMBLED = "Assembled"
    QUALITY_CHECKED = "Quality Checked"
    PACKED = "Packed"
    STORED = "Stored"
    DELIVERED= "Delivered"

class Furniture:
    def __init__(self, type: str, materials: List[Material]):
        self.type = type
        self.materials = materials
        self.status: FurnitureState = FurnitureState.CREATED
    @property
    def type(self)->str:
        return self._type
    @type.setter
    def type(self,value:str):
        if not value:
            raise InvalidDataError
        self._type=value
    @property
    def status(self)->FurnitureState:
        return self._status
    @status.setter
    def status(self,value:FurnitureState):
        if not isinstance(value,FurnitureState):
            raise InvalidDataError("Status must be from FurnitureState")
        self._status=value
    @property
    def material_count(self)->int:
        return len(self.materials)
    @property
    def material_names(self)->List[str]:
        return [m.name for m in self.materials]

    def get_material_by_name(self, name: str) -> Material:
        for material in self.materials:
            if material.name == name:
                return material
        raise InvalidDataError(f"Material '{name}' not found")

    def change_status(self, new_status: FurnitureState) -> None:
        self.status = new_status

    
