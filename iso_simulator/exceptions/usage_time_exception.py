class UsageTimeError(Exception):
    """Raised when something went wrong with the function getUsagetime()"""

    def __init__(self, value: str):
        self.value = value
