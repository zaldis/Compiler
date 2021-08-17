class InvalidSyntaxError(Exception):
    def __init__(self, position, message="Wrong character"):
        self.position = position
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}: {self.position}.'