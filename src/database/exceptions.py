class NoConnectionError(BaseException):
    def __init__(self, message: str = "Нет соединения с базой данных"):
        self.message = message 
        super().__init__(self.message)
    