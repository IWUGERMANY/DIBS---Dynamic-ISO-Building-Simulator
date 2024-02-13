class GHGEmissionError(Exception):
    """Raised when an error occured during calculation of GHG-Emission for Heating. The following heating_supply_system cannot be considered yet"""

    def __int__(self, value: str):
        self.value = value
