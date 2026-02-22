from abc import ABC
from .exceptions import InvalidDataError,InvalidAmountError




class Material(ABC):
    def __init__(self,amount:float):
        self.amount=amount
        self._is_busy=False
    @property
    def amount(self)->float:
        return self._amount
    @amount.setter
    def amount(self,value:float):
        if value is None:
            raise InvalidAmountError("Amount can't be empty")
        if value<=0:
            raise InvalidAmountError("Amount must be positive")
        self._amount=value
    @property
    def is_busy(self)->bool:
        return self._is_busy
    @is_busy.setter
    def is_busy(self,value:bool):
        if not isinstance(value,bool):
            raise InvalidDataError("Type must be a boolean")
        self._is_busy=value

class Metal(Material):
    def __init__(self, type: str, amount: float):
        super().__init__(amount)
        self.type=type

    @property
    def type(self)->str:
        return self._type
    
    @type.setter
    def type(self,value:str):
        if not value:
            raise InvalidDataError("Metal type can't be empty")
        self._type=value
    
    def __str__(self) -> str:
        return f'Metal type: {self.type}, amount: {self.amount}'

class Wood(Material):
    def __init__(self,type:str,amount:float):
        super().__init__(amount)
        self.type=type
    @property
    def type(self)->str:
        return self._type
    
    @type.setter
    def type(self,value:str):
        if not value:
            raise InvalidDataError("Wood type can't be empty")
        self._type=value
    
    def __str__(self) -> str:
        return f'Wood type: {self.type}, amount: {self.amount}'
