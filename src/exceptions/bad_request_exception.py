
class BadRequestException(Exception):
    def __init__(self, message="An error occurred."):
        self.message = message
        self.error_code = 400
        super().__init__(self.message)
    
    def __str__(self) -> str:
        return str(self.__dict__)

        