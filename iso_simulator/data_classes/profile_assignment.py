class ProfilesAssignment:

    def __init__(self,
                 hk_geb: str,
                 uk_geb: str,
                 typ_18599: str,
                 nr_18599: float,
                 typ_sia2024: str,
                 nr_sia2024: float,
                 gain_per_person_18599: int,
                 gain_per_person_sia2024: int,
                 appliance_gains_tief_18599: float,
                 appliance_gains_mittel_18599: float,
                 appliance_gains_hoch_18599: float,
                 appliance_gains_ziel_sia2024: float,
                 appliance_gains_standard_sia2024: int,
                 appliance_gains_bestand_sia2024: float,
                 usage_start_18599: int,
                 usage_end_18599: int,
                 usage_start_sia2024: int,
                 usage_end_sia2024: int
                 ):

        self.hk_geb = hk_geb
        self.uk_geb = uk_geb
        self.typ_18599 = typ_18599
        self.nr_18599 = nr_18599
        self.typ_sia2024 = typ_sia2024
        self.nr_sia2024 = nr_sia2024
        self.gain_per_person_18599 = gain_per_person_18599
        self.gain_per_person_sia2024 = gain_per_person_sia2024
        self.appliance_gains_tief_18599 = appliance_gains_tief_18599
        self.appliance_gains_mittel_18599 = appliance_gains_mittel_18599
        self.appliance_gains_hoch_18599 = appliance_gains_hoch_18599
        self.appliance_gains_ziel_sia2024 = appliance_gains_ziel_sia2024
        self.appliance_gains_standard_sia2024 = appliance_gains_standard_sia2024
        self.appliance_gains_bestand_sia2024 = appliance_gains_bestand_sia2024
        self.usage_start_18599 = usage_start_18599
        self.usage_end_18599 = usage_end_18599
        self.usage_start_sia2024 = usage_start_sia2024
        self.usage_end_sia2024 = usage_end_sia2024
