from datasource import DataSource
import sys,os,pandas as pd
from geopy.distance import geodesic
from typing import List, Tuple, Union
mainPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, mainPath)

from model.auxiliary_methods import *
from model.building import Building
from model.primary_energy_and_emission_factors import PrimaryEnergyAndEmissionFactor
from model.weather_data import WeatherData
from model.plz_data import PLZData
from model.weatherfiles_stations import WeatherStation109, WeatherStation93
from model.epw_file import EPWFile

# from building_physics import Building


class DataSourceCSV(DataSource):

    def getBuildingData(self) -> Building:
        building_data = pd.read_csv(
            'SimulationData_Breitenerhebung.csv', sep=';', index_col=False, encoding='utf8')
        first_building = building_data.iloc[0].values
        return Building(*first_building)

    def getEPW_PE_Factors(self) -> List[PrimaryEnergyAndEmissionFactor]:
        GWP_PE_Factors = pd.read_csv(
            'LCA/Primary_energy_and_emission_factors.csv', sep = ';', decimal=',', index_col = False, encoding = 'cp1250')
        
        list_of_gwp_pe_factors_objects = []

        for index, row in GWP_PE_Factors.iterrows():
            my_object = PrimaryEnergyAndEmissionFactor(*row.values)
            list_of_gwp_pe_factors_objects.append(my_object)
        return list_of_gwp_pe_factors_objects
    
    # def getEPWFile(self, plz, weather_period):
    #     plz_data = pd.read_csv(os.path.join('../auxiliary/weather_data/plzcodes.csv'), encoding = 'latin', dtype={'zipcode': int})

    #     list_of_plz_data_objects: List[PLZData] = []
    #     list_weather_station = []

    #     for index, row in plz_data.iterrows():
    #         my_object = PLZData(*row.values)
    #         list_of_plz_data_objects.append(my_object)

    #     if (weather_period == "2007-2021"):
    #          weatherfiles_stations = pd.read_csv(os.path.join('../auxiliary/weather_data/weather_data_TMYx_2007_2021/weatherfiles_stations_109.csv'), sep = ';')
    #          for index, row in weatherfiles_stations.iterrows():
    #              my_object = WeatherStation109(*row.values)
    #              list_weather_station.append(my_object)
    #     else:
    #         weatherfiles_stations = pd.read_csv(os.path.join('../auxiliary/weather_data/weatherfiles_stations_93.csv'), sep = ';')
    #         for index, row in weatherfiles_stations.iterrows():
    #             my_object = WeatherStation93(*row.values)
    #             list_weather_station.append(my_object)
        
    #     coordinates_plz = getCoordinatesByPLZ(list_of_plz_data_objects, plz)
    #     logging.info(f"My value list coordinate is : {coordinates_plz}")

    #     logging.warning(list_weather_station[0].latitude_building)
    #     logging.warning(coordinates_plz)

    #     for item in list_weather_station:
    #         item.latitude_building = coordinates_plz[0]
    #         item.longitude_building = coordinates_plz[1]
        
    #     # Calculate minimum distance to next weather station
    #     for station in list_weather_station:
    #         distance = geodesic((station.latitude, station.longitude),
    #                             (station.latitude_building, station.longitude_building)).km
    #         station.distance = distance
        
    #     min_distance_station = min(list_weather_station, key=lambda x: x.distance)
    #     epw_filename = min_distance_station.filename
    #     coordinates_station = [min_distance_station.latitude, min_distance_station.longitude]
    #     distance = min_distance_station.distance

    #     return epw_filename, coordinates_station, distance


    def getWeatherData(self, epwfile_path) -> List[WeatherData]:
        weather_data = pd.read_csv(
            epwfile_path, skiprows=8, header=None).drop('datasource', axis=1)
        
        list_of_weather_data_objects = []

        for index, row in weather_data.iterrows():
            my_object = WeatherData(*row.values)
            list_of_weather_data_objects.append(my_object)
        return list_of_weather_data_objects
     
    def getEPWFile(self, plz, weather_period) -> EPWFile:
        """
        Function finds the epw file depending on building location
        

        :external input data: File with german zip codes [../auxiliary/weather_data/plzcodes.csv]
                              File with metadata of weather stations (e.g. longitude, latitude) [../auxiliary/weather_data/weatherfiles_stations_93.csv]
        
        :return epw_filename: filename of the epw
        :rtype: tuple (string)
        :return coordinates_station: latitude and longitute of the selected station
        :rtype: tuple (float)
        """

        list_weather_station = []

        # Read data
        plz_data = pd.read_csv(os.path.join('../auxiliary/weather_data/plzcodes.csv'), encoding = 'latin', dtype={'zipcode': int})

        if (weather_period == "2007-2021"):
            weatherfiles_stations = pd.read_csv(os.path.join('../auxiliary/weather_data/weather_data_TMYx_2007_2021/weatherfiles_stations_109.csv'), sep = ';')
            weatherfiles_stations_objects: List[WeatherStation109] = [WeatherStation109(*row.values) for _, row in weatherfiles_stations.iterrows()]
        else:      
            weatherfiles_stations = pd.read_csv(os.path.join('../auxiliary/weather_data/weatherfiles_stations_93.csv'), sep = ';')
            weatherfiles_stations_objects: List[WeatherStation93] = [WeatherStation93(*row.values) for _, row in weatherfiles_stations.iterrows()]


        # Pick latitude and longitude from plz_data and put values into a list
        coordinates_plz = plz_data.loc[plz_data['zipcode'] == plz, ['latitude', 'longitude']].iloc[0].tolist()

        # Append plz to weatherfiles_stations
        weatherfiles_stations['latitude_building'], weatherfiles_stations['longitude_building'] = coordinates_plz

        # Calculate minimum distance to next weather station
        weatherfiles_stations['distance'] = weatherfiles_stations.apply(lambda x: geodesic((x['latitude'], x['longitude']),
                                                   (x['latitude_building'], x['longitude_building'])).km, axis = 1)

        # Pick filename of minimum distance
        epw_filename = weatherfiles_stations.loc[weatherfiles_stations['distance'].idxmin(), 'filename']    

        # Pick latitude and longitude from station as arguments in calc_sun_position(), See annualSimulation.py
        coordinates_station = weatherfiles_stations.loc[weatherfiles_stations['distance'].idxmin(), ['latitude', 'longitude']].tolist() 

        # Distance 
        distance = weatherfiles_stations.loc[weatherfiles_stations['distance'].idxmin(), 'distance']

        return EPWFile(epw_filename, coordinates_station, distance)









# b = DataSourceCSV().getBuildingData()
# print(b)

# x = DataSourceCSV().getEPW_PE_Factors()
x = DataSourceCSV().getEPWFile(99734, "2007-2021")

print(x.file_name)
print(x.coordinates_station)
print(x.distance)