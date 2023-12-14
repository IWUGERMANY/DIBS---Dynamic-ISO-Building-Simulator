class PrimaryEnergyAndEmissionFactor:

    def __init__(self,
                 energy_carrier: str,
                 primary_energy_factor_GEG: float,
                 relation_calorific_to_heating_value_GEG: float,
                 gwp_spezific_to_heating_value_GEG: int,
                 use: str
                 ):
        self.energy_carrier = energy_carrier
        self.primary_energy_factor_GEG = primary_energy_factor_GEG
        self.relation_calorific_to_heating_value_GEG = relation_calorific_to_heating_value_GEG
        self.gwp_spezific_to_heating_value_GEG = gwp_spezific_to_heating_value_GEG
        self.use = use
