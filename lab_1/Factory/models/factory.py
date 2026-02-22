from .furniture import Furniture
from typing import List
from .people import Worker
from .tool import Tool
from operations.operations import Operation
from .exceptions import InvalidDataError
class Factory:
    def __init__(self, factory_type: str, workers: List[Worker], tools: List[Tool], operation: Operation):
        self.factory_type = factory_type  
        self.workers = workers
        self.tools = tools
        self.operation = operation

    @property
    def factory_type(self) -> str:
        return self._factory_type
    
    @factory_type.setter
    def factory_type(self, value: str):
        if not value:
            raise InvalidDataError("Factory type can't be empty")
        self._factory_type = value

    def process(self, furniture: Furniture) -> None:
        available_worker = Worker.find_available(self.workers)
        if not available_worker:
            raise InvalidDataError(f"No available workers in {self._factory_type} factory")
        
        available_tool = Tool.find_available(self.tools)  
        if not available_tool:
            raise InvalidDataError(f"No available tools in {self._factory_type} factory")
        available_worker.is_busy = True
        available_tool.use()
        self.operation.execute(furniture)
        available_worker.is_busy = False
        
        print(f'  {self._factory_type} factory processed {furniture.type}')
        print(f'   Worker: {available_worker.name}')
        print(f'   Tool: {available_tool.name}')
        print(f'   Status: {furniture.status.value}')