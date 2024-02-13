class PLZNotFoundError(Exception):
    """Raised when zipcode not found"""

    def __int__(self):
        self.value = "Zipcode not found"
