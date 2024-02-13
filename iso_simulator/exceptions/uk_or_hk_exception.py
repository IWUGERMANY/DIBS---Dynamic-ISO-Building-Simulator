class HkOrUkNotFoundError(Exception):
    """Raised when hk_geb or uk_geb not found in the dataframe"""

    def __int__(self, value: str):
        self.value = value
