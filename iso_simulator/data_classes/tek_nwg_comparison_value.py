class TekNwgComparisonValue:

    def __init__(self,
                 tek_category: str,
                 tek_heating: float,
                 tek_hotwater: float,
                 tek_ventilation: float,
                 tek_builtin_lighting: float,
                 tek_cold: float,
                 tek_auxiliary_energy_for_cold: float,
                 tek_dehumidification: float,
                 tek_other: float,
                 lfd_nr: int
                 ):

        self.tek_category = tek_category
        self.tek_heating = tek_heating
        self.tek_hotwater = tek_hotwater
        self.tek_ventilation = tek_ventilation
        self.tek_builtin_lighting = tek_builtin_lighting
        self.tek_cold = tek_cold
        self.tek_auxiliary_energy_for_cold = tek_auxiliary_energy_for_cold
        self.tek_dehumidification = tek_dehumidification
        self.tek_other = tek_other
        self.lfd_nr = lfd_nr
