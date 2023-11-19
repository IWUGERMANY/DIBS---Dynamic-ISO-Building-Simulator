from typing import Tuple, Union, List

"""
This class is an object from a data set in the file 'TEK_NWG_Vergleichswerte.csv'
"""


class TekNwgComparisonValue:

    def __init__(self,
                 TEK_category: str,
                 TEK_heating: float,
                 TEK_hotwater: float,
                 TEK_ventilation: float,
                 TEK_builtin_lighting: float,
                 TEK_cold: float,
                 TEK_auxiliary_energy_for_cold: float,
                 TEK_dehumidification: float,
                 TEK_other: float,
                 lfd_nr: int
                 ):

        self.TEK_category = TEK_category
        self.TEK_heating = TEK_heating
        self.TEK_hotwater = TEK_hotwater
        self.TEK_ventilation = TEK_ventilation
        self.TEK_builtin_lighting = TEK_builtin_lighting
        self.TEK_cold = TEK_cold
        self.TEK_auxiliary_energy_for_cold = TEK_auxiliary_energy_for_cold
        self.TEK_dehumidification = TEK_dehumidification
        self.TEK_other = TEK_other
        self.lfd_nr = lfd_nr

    def get_tek_dhw_and_category(self, TEK_name: str) -> float:
        """
        Find the TEK_dhw

        :param TEK_name: 
        :type TEK_name: string

        :return: TEK_dhw
        :rtype: float
        """

        if self.TEK_category == TEK_name:
            TEK_dhw = float(self.TEK_hotwater)
            return TEK_dhw
        else:
            return None


"""
This class is an object from a data set in the file 'TEK_NWG_Vergleichwerte_zuweisung.csv'
"""


class TekNwgComparisonValueAssignment:

    def __init__(self,
                 hk_geb: str,
                 uk_geb: str,
                 TEK: str
                 ):

        self.hk_geb = hk_geb
        self.uk_geb = uk_geb
        self.TEK = TEK

    def getTEK(self, nwg_comparison_value: TekNwgComparisonValue) -> Union[Tuple[float, str], str]:
        """
        Find TEK_dhw and TEK_name values from Teilenergiekennwerte zur Bildung der Vergleichswerte gemäß der Bekanntmachung vom 15.04.2021 zum Gebäudeenergiegesetz (GEG) vom 2020, 
        depending on hk_geb, uk_geb


        :external input data: ../auxiliary/TEKs/TEK_NWG_Vergleichswerte.csv


        :param hk_geb: usage type (from the constructor)
        :type hk_geb: string
        :param uk_geb: usage type (from the constructor)
        :type uk_geb: string

        :return: df_TEK, TEK_name
        :rtype: DataFrame (with floats), string
        """

        if self.hk_geb is None and self.uk_geb is None:
            TEK_name = str(self.TEK)
            TEK_dhw = nwg_comparison_value.get_tek_dhw_and_category(TEK_name)
            return TEK_dhw, TEK_name
        else:
            return 'uk_geb unbekannt oder kh_geb unbekannt'

    def getTekData(self, nwg_comparison_values: List[TekNwgComparisonValue]) -> Union[Tuple[float, str], str]:
        for nwg_comparison_value in nwg_comparison_values:
            TEK_name = self.TEK
            if nwg_comparison_value.TEK_category == TEK_name:
                TEK_dhw = nwg_comparison_value.TEK_hotwater
                return float(TEK_dhw), TEK_name
        return 'uk_geb unbekannt oder kh_geb unbekannt'
