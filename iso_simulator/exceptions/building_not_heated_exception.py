class BuildingNotHeatedError(Exception):
    """Raised when the building not heated"""

    def __int__(self, value: str):
        self.value = value
