class BadRequestException(Exception):
    def __init__(self, message:str ="An error occurred."):
        self.message:str = message
        self.error_code:int = 400
        super().__init__(self.message)
    
    def __str__(self) -> str:
        return str(self.__dict__)

        