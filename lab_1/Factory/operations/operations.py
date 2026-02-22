from abc import ABC, abstractmethod
from models.furniture import Furniture, FurnitureState
import random
from models.people import Worker
from models. warehouse import Warehouse
from typing import List
from models.tool import Tool
from models.exceptions import InvalidOperation, InvalidAmountError
from datetime import datetime

class Operation(ABC):
    @abstractmethod
    def execute(self, furniture: Furniture) -> None:
        pass


class PreparationOperation(Operation):
    def __init__(self, warehouse: Warehouse, workers: List[Worker], tools: List[Tool]):
        self.warehouse = warehouse
        self.workers = workers  
        self.tools = tools      
    
    def execute(self, furniture: Furniture) -> None:
        if furniture.status != FurnitureState.CREATED:
            raise InvalidOperation("Materials can only be prepared for new furniture")
        
        available_worker = Worker.find_available(self.workers)
        if not available_worker:
            raise InvalidAmountError("No available workers for preparation")
        
        available_tool = Tool.find_available(self.tools)
        if not available_tool:
            raise InvalidAmountError("No available tools for preparation")
        
        metal_needed = 0.0
        wood_needed = 0.0
        
        for material in furniture.materials:
            if material.__class__.__name__ == "Metal":
                metal_needed += material.amount
            elif material.__class__.__name__ == "Wood":
                wood_needed += material.amount
        
        if metal_needed > self.warehouse.metal_amount:
            raise InvalidAmountError(f"Not enough metal. Need {metal_needed}, have {self.warehouse.metal_amount}")
        
        if wood_needed > self.warehouse.wood_amount:
            raise InvalidAmountError(f"Not enough wood. Need {wood_needed}, have {self.warehouse.wood_amount}")

        available_worker.is_busy = True
        available_tool.use()
        
        furniture.change_status(FurnitureState.MATERIALS_PREPARED)
        
        available_worker.is_busy = False
        
        print(f"   Materials prepared for {furniture.type}")
        print(f"   Worker: {available_worker.name}")
        print(f"   Tool: {available_tool.name}")
        print(f"   Metal needed: {metal_needed}")
        print(f"   Wood needed: {wood_needed}")
        print(f"   Status: {furniture.status}")


class CreateElementOperation(Operation):
    def __init__(self, warehouse: Warehouse, workers: List[Worker], tools: List[Tool]):
        self.warehouse = warehouse
        self.workers = workers
        self.tools = tools
    
    def execute(self, furniture: Furniture) -> None:
        if furniture.status != FurnitureState.MATERIALS_PREPARED:
            raise InvalidOperation("Materials must be prepared first")
        
        available_tool = Tool.find_available(self.tools)
        if not available_tool: 
            raise InvalidAmountError("No available tools for work")
        
        available_worker = Worker.find_available(self.workers)
        if not available_worker: 
            raise InvalidAmountError("No available workers")
        
        metal_needed = 0.0
        wood_needed = 0.0
        
        for material in furniture.materials:
            if material.__class__.__name__ == "Metal":
                metal_needed += material.amount
            elif material.__class__.__name__ == "Wood":
                wood_needed += material.amount
        
        if metal_needed > self.warehouse.metal_amount:
            raise InvalidAmountError(f"Not enough metal. Need {metal_needed}, have {self.warehouse.metal_amount}")
        
        if wood_needed > self.warehouse.wood_amount:
            raise InvalidAmountError(f"Not enough wood. Need {wood_needed}, have {self.warehouse.wood_amount}")
        
        self.warehouse.metal_amount -= metal_needed
        self.warehouse.wood_amount -= wood_needed
        
        available_worker.is_busy = True
        available_tool.use()
        
        furniture.change_status(FurnitureState.ELEMENTS_MANUFACTURED)
        
        available_worker.is_busy = False
        
        print(f"   Elements manufactured for {furniture.type}")
        print(f"   Worker: {available_worker.name}")
        print(f"   Tool: {available_tool.name}")
        print(f"   Metal used: {metal_needed}")
        print(f"   Wood used: {wood_needed}")
        print(f"   Status: {furniture.status}")


class AssemblyOperation(Operation):
    def __init__(self, warehouse: Warehouse, workers: List[Worker]):
        self.warehouse = warehouse
        self.workers = workers
    
    def execute(self, furniture: Furniture) -> None:
        if furniture.status != FurnitureState.ELEMENTS_MANUFACTURED:
            raise ValueError("Cannot assemble: elements must be manufactured first")
        
        available_worker = Worker.find_available(self.workers)
        if not available_worker: 
            raise InvalidAmountError("No available workers for assembly")
        
        available_worker.is_busy = True
        furniture.change_status(FurnitureState.ASSEMBLED)
        
        available_worker.is_busy = False
        
        print(f"   Assembled {furniture.type}")
        print(f"   Worker: {available_worker.name}")
        print(f"   Status: {furniture.status}")


class CheckOperation(Operation):
    def __init__(self, inspector: Worker, workers: List[Worker] = None):
        self.inspector = inspector
        self.workers = workers if workers else []
    
    def execute(self, furniture: Furniture) -> None:
        if furniture.status != FurnitureState.ASSEMBLED:
            raise InvalidOperation("Can't check quality before assembly")
        
        inspector = self.inspector
        if not inspector:
            raise InvalidOperation("No inspector available")
        
        if inspector.is_busy:
            raise InvalidOperation(f"Inspector {inspector.name} is busy")
        
        inspector.is_busy = True
        
        possible_defects = ["Scratch", "Crack", "Paint issue", "Loose screw"]
        num_defects = random.randint(0, 3)
        
        if num_defects > 0:
            defects = random.sample(possible_defects, num_defects)
        else:
            defects = []
        
        score = random.randint(50, 100)
        passed = score >= 70
        
        furniture.quality_score = score
        furniture.defects = defects
        furniture.inspector_name = inspector.name
        
        if passed:
            furniture.change_status(FurnitureState.QUALITY_CHECKED)
            print(f"   Quality check PASSED for {furniture.type}")
        else:
           
            furniture.quality_failed = True  
            furniture.change_status(FurnitureState.ELEMENTS_MANUFACTURED)  
    
            print(f"   Quality check FAILED for {furniture.type}")
            print(f"   Defects: {', '.join(defects)}")
            print("   Нужно запустить производство заново для исправления")
        
        print(f"   Score: {score}")
        print(f"   Inspector: {inspector.name}")
        
        inspector.is_busy = False
class PackingOperation(Operation):
    def __init__(self, packer: Worker, workers: List[Worker] = None):
        self.packer = packer
        self.workers = workers if workers else []
    
    def execute(self, furniture: Furniture):
        if furniture.status != FurnitureState.QUALITY_CHECKED:
            raise ValueError("Can't pack before quality check")
        
        packer = self.packer
        if not packer and self.workers:
            packer = Worker.find_by_specialization(self.workers, "packer")
        
        if not packer:
            raise InvalidOperation("No packer available")
        
        if packer.is_busy:
            raise InvalidOperation(f"Packer {packer.name} is busy")
        
        packer.is_busy = True
        
        possible_packing_material = ["Paper", "Box", "Film"]
        num_packing_material = random.randint(1, 3) 
        packing_material = random.sample(possible_packing_material, num_packing_material)
        
        furniture.packing_material = packing_material
        furniture.packer_name = packer.name
        
        furniture.change_status(FurnitureState.PACKED)
        
        packer.is_busy = False
        
        print(f"   Packed {furniture.type}")
        print(f"   Packing materials: {', '.join(packing_material)}")
        print(f"   Packer: {packer.name}")
        print(f"   Status: {furniture.status}")


class DeliveryOperation(Operation):
    def __init__(self, delivery_man: Worker, address: str = None, workers: List[Worker] = None):
        self.delivery_man = delivery_man
        self.address = address
        self.workers = workers if workers else []
    
    def execute(self, furniture: Furniture):
        if furniture.status != FurnitureState.PACKED:
            raise InvalidOperation("Can't deliver before packing")
        
        delivery_man = self.delivery_man
        if not delivery_man and self.workers:
            delivery_man = Worker.find_by_specialization(self.workers, "driver")
        
        if not delivery_man:
            raise InvalidOperation("No delivery man available")
        
        if delivery_man.is_busy:
            raise InvalidOperation(f"Delivery man {delivery_man.name} is busy")
        
        if not self.address and not hasattr(furniture, 'delivery_address'):
            raise InvalidOperation("No delivery address specified")
        
        delivery_man.is_busy = True
        
        delivery_address = self.address or getattr(furniture, 'delivery_address', 'Unknown')
        
        furniture.delivery_man_name = delivery_man.name
        furniture.delivery_address = delivery_address
        furniture.delivery_date = datetime.now()
        
        furniture.change_status(FurnitureState.DELIVERED)
        
        self.workshop.add_completed_furniture(furniture)
        
        delivery_man.is_busy = False
        
        print(f"   Delivered {furniture.type}")
        print(f"   Delivery man: {delivery_man.name}")
        print(f"   Address: {delivery_address}")
        print(f"   Date: {furniture.delivery_date.strftime('%Y-%m-%d %H:%M')}")
        print(f"   Status: {furniture.status}")
        print(f"   Stored in: {self.workshop.workshop_type}")