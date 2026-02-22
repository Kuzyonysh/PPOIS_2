from .exceptions import InvalidDataError,InvalidAmountError
class Order:
    def __init__(self, type: str, amount: int):
        self.type = type
        self.quantity = amount
    @property
    def type(self)->str:
        return self._type
    @type.setter
    def type(self,value:str):
        if not value:
            raise InvalidDataError("Type cant't be empty")
        self._type=value
    @property
    def amount(self)->int:
        return self._amount
    @amount.setter
    def amount(self,value:int):
        if value is None:
            raise InvalidAmountError("Amount can't be empty")
        if value<=0:
            raise InvalidAmountError("Amount must be positive")
        self._amount=value
    