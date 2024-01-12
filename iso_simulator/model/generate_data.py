from iso_simulator.data_source.datasource_csv import DataSourceCSV


class GenerateData:

    def __init__(self, datasource: DataSourceCSV, weather_period: str):
        self.datasource = datasource
        self.weather_period = weather_period
        self.all_buildings = self.get_all_buildings()
        self.gwp_PE_Factors = datasource.get_epw_pe_factors()

    def get_all_buildings(self):
        return self.datasource.get_all_buildings()

    def get_epw_pe_factors(self):
        return self.datasource.get_epw_pe_factors()

    def filter_building_by_src_id(self, building_id: str):
        for building in self.all_buildings:
            if building.scr_gebaeude_id == building_id:
                return building
