class CustomException(Exception):
    """A custom exception class to handle application errors.

    Attributes:
        code (int): The HTTP status code for the error.
        message (str): A human-readable message for the error.
        data (list): Additional data about the error.
    """

    def __init__(self, message="", code=400):
        self.code = code
        self.message = message
        super().__init__(message) 
