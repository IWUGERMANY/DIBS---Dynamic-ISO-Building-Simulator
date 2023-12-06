from typing import List
from geopy.distance import geodesic

from iso_simulator.model.weatherfiles_stations import WeatherStation109, WeatherStation93
import pandas as pd
import os


def get_weather_files_stations(weather_period: str) -> pd.DataFrame:

    if (weather_period == "2007-2021"):
        weatherfiles_stations = pd.read_csv(os.path.join(
            'iso_simulator/auxiliary/weather_data/weather_data_TMYx_2007_2021/weatherfiles_stations_109.csv'), sep=';')
        weatherfiles_stations_objects: List[WeatherStation109] = [
            WeatherStation109(*row.values) for _, row in weatherfiles_stations.iterrows()]
    else:
        weatherfiles_stations = pd.read_csv(os.path.join(
            'iso_simulator/auxiliary/weather_data/weatherfiles_stations_93.csv'), sep=';')
        weatherfiles_stations_objects: List[WeatherStation93] = [
            WeatherStation93(*row.values) for _, row in weatherfiles_stations.iterrows()]
    return weatherfiles_stations


def get_coordinates_plz(plz_data: pd.DataFrame, plz: str) -> List:
    return plz_data.loc[plz_data['zipcode'] == plz, [
        'latitude', 'longitude']].iloc[0].tolist()


def calculate_minimum_distance_to_next_weather_station(weatherfiles_stations: pd.DataFrame) -> None:
    weatherfiles_stations['distance'] = weatherfiles_stations.apply(lambda x: geodesic((x['latitude'], x['longitude']),
                                                                                       (x['latitude_building'], x['longitude_building'])).km, axis=1)


def get_filename_with_minimum_distance(weatherfiles_stations: pd.DataFrame) -> str:
    return weatherfiles_stations.loc[weatherfiles_stations['distance'].idxmin(
    ), 'filename']


def get_coordinates_station(weatherfiles_stations: pd.DataFrame) -> List:
    return weatherfiles_stations.loc[weatherfiles_stations['distance'].idxmin(), [
        'latitude', 'longitude']].tolist()


def get_distance(weatherfiles_stations: pd.DataFrame) -> float:
    return weatherfiles_stations.loc[weatherfiles_stations['distance'].idxmin(
    ), 'distance']
