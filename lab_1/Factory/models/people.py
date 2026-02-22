from abc import ABC, abstractmethod
from .exceptions import InvalidDataError
from typing import List
from .orders import Order

class People(ABC):
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
        self._is_busy = False  # ← ВАЖНО!
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str):
        if not value:
            raise InvalidDataError("Name can't be empty.")
        self._name = value

    @property
    def age(self) -> int:
        return self._age
    
    @age.setter
    def age(self, value: int): 
        if value < 0 or value > 150:
            raise InvalidDataError("Age must be between 0 and 150")
        self._age = value
    
    @property
    def is_busy(self) -> bool:
        return self._is_busy
    
    @is_busy.setter
    def is_busy(self, value: bool):
        if not isinstance(value, bool):
            raise InvalidDataError("is_busy must be a boolean")
        self._is_busy = value

    @abstractmethod
    def get_role(self) -> str:
        pass
    
    @abstractmethod
    def work(self) -> str:
        pass
class Worker(People):
    def __init__(self,name:str,age:int,specialization:str,experience:int):
        super().__init__(name,age)
        self.specialization=specialization
        self.experience=experience
    
    @property
    def specialization(self)->str:
        return self._specialization
    
    @specialization.setter
    def specialization(self,value:str):
        if not value:
            raise InvalidDataError("Specialization can't be empty")
        self._specialization=value
    
    @property
    def experience(self)->int:
        return self._experience
    
    @experience.setter
    def experience(self,value:int):
        self._experience=value

    def __str__(self)->str:
        return f'{self.name} ready to work'

    def get_role(self)->str:
        return "Worker"
    
    def work(self)->str:
        return f'{self.name} is working as {self.specialization}'
    @staticmethod
    def find_available(workers):  
            for worker in workers:  
                if not worker.is_busy:  
                    return worker
            return None
class Customer(People):
    def __init__(self, name: str, age: int, phone: str, order:str=None):
        super().__init__(name, age)
        self.phone = phone
        self.orders:List[Order]=[]
    @property
    def phone(self)->str:
        return self._phone
    
    @phone.setter
    def phone(self,value:str):
        if not value:
            raise InvalidDataError("Phone number can't be empty")
        self._phone=value

    def __str__(self)->str:
        return f'{self.name} ready to make an order'
    
    def get_role(self)->str:
        return "Customer"
    def work(self) -> str:
        if self.orders:
            return f"{self.name} places an order"
        return f"{self.name} chooses staff"
    
    def make_order(self, type: str, amount: int)->Order:
        order = Order(type, amount)
        self.orders.append(order)
        print(f"{self.name} made an order: {order}")
        return order
        