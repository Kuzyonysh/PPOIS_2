from .exceptions import InvalidAmountError,InvalidDataError
class Tool:
    def __init__(self, name: str, durability: int):
        self.name = name
        self.durability = durability
    
    @property
    def name(self)->str:
        return self._name
    @name.setter
    def name(self,value:str):
        if not value:
            raise InvalidDataError("Name can't be empty")
        self._name=value
    @property
    def durability(self)->int:
        return self._durability
    @durability.setter
    def durability(self,value:int):
        if not isinstance(value, int):
            raise InvalidAmountError("Durability must be an integer")
        if value<=0:
            raise InvalidAmountError("Durability must be positive")
        self._durability=value
    @property
    def is_broken(self)->bool:
        return self._durability<=0
    def use(self) -> str:
        if self.is_broken:
            raise ValueError(f"Tool {self.name} is broken")
        self.durability -= 1
        if self.is_broken:
            return f"Tool '{self.name}' broke after this use"
        return f"Used tool '{self.name}'. Durability left: {self._durability}"

    def repair(self,amount:int=None)->str:
        if amount is None:
            self._durability=100
            return f'Tool {self.name} fully repaired'
        if not isinstance(amount,int):
            raise InvalidAmountError("Repair amount must be an integer")
        if amount<=0:
            raise InvalidAmountError("Amount must be positive")
        self._durability+=amount
        return f"Tool '{self.name}' repaired by {amount}. Now: {self._durability}"

    @staticmethod
    def find_available(tools):  
            for tool in tools:
             if not tool.is_broken:
                    return tool
            return None
    def __str__(self) -> str:
        status = "BROKEN" if self.is_broken else f"durability: {self._durability}"
        return f'Tool: {self.name} [{status}]'
