"""
This class is an object from a data set in the file 'profiles_zuweisungen.csv'
"""

from typing import Tuple


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

    def getGains(self, profile_from_norm: str, gains_from_group_values: str) -> Tuple[float, float, str]:
        """
        Find data from DIN V 18599-10 or SIA2024


        :external input data: Assignments [../auxiliary/norm_profiles/profiles_zuweisungen.csv]

        :param hk_geb: usage type (value from constructor)
        :type hk_geb: string
        :param uk_geb: usage type (value from constructor)
        :type uk_geb: string
        :param profile_from_norm: data source either 18599-10 or SIA2024 [specified in annualSimulation.py]
        :type profile_from_norm: string
        :param gains_from_group_values: group in norm low/medium/high [specified in annualSimulation.py]
        :type gains_from_group_values: string

        :return: gain_per_person, appliance_gains, typ_norm
        :rtype: tuple (float, float, string)
        """

        if self.hk_geb is not None and self.uk_geb is not None:

            if profile_from_norm == 'sia2024':
                typ_norm = self.typ_sia2024.strip()
                gain_per_person = float(self.gain_per_person_sia2024.strip())

                if gains_from_group_values == 'low':
                    appliance_gains = float(
                        self.appliance_gains_ziel_sia2024.strip())

                elif gains_from_group_values == 'mid':
                    appliance_gains = float(
                        self.appliance_gains_standard_sia2024.strip())

                elif gains_from_group_values == 'max':
                    appliance_gains = float(
                        self.appliance_gains_bestand_sia2024.strip())

            elif profile_from_norm == 'din18599':

                typ_norm = self.typ_18599.strip()
                gain_per_person = float(self.gain_per_person_18599.strip())

                if gains_from_group_values == 'low':
                    appliance_gains = float(
                        self.appliance_gains_tief_18599.strip())

                elif gains_from_group_values == 'mid':
                    appliance_gains = float(
                        self.appliance_gains_mittel_18599.strip())

                elif gains_from_group_values == 'max':
                    appliance_gains = float(
                        self.appliance_gains_hoch_18599.strip())

        return gain_per_person, appliance_gains, typ_norm