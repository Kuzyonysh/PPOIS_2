class InvalidDataError(Exception):
    def __init__(self,msg:str)->None:
        super().__init__(msg)

class InvalidAmountError(Exception):
    def __init__(self,msg:str)->None:
        super().__init__(msg)

class InvalidOperation(Exception):
    def __init__(self,msg:str)->None:
        super().__init__(msg)