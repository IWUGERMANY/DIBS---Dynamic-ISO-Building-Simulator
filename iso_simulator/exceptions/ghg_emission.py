class GHGEmissionException(Exception):
    def __int__(self, message: str = "Error occured during calculation of GHG-Emission for Heating. The following heating_supply_system cannot be considered yet"):
        self.message = message
        super().__init__(self.message)