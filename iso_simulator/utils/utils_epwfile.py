from typing import List
from model.weatherfiles_stations import WeatherStation109, WeatherStation93
import sys
import os
import pandas as pd
from geopy.distance import geodesic

mainPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, mainPath)


def getWeatherFilesStations(weather_period):

    if (weather_period == "2007-2021"):
        weatherfiles_stations = pd.read_csv(os.path.join(
            '../auxiliary/weather_data/weather_data_TMYx_2007_2021/weatherfiles_stations_109.csv'), sep=';')
        weatherfiles_stations_objects: List[WeatherStation109] = [
            WeatherStation109(*row.values) for _, row in weatherfiles_stations.iterrows()]
    else:
        weatherfiles_stations = pd.read_csv(os.path.join(
            '../auxiliary/weather_data/weatherfiles_stations_93.csv'), sep=';')
        weatherfiles_stations_objects: List[WeatherStation93] = [
            WeatherStation93(*row.values) for _, row in weatherfiles_stations.iterrows()]
    return weatherfiles_stations


def getCoordinatesPlz(plz_data, plz):
    return plz_data.loc[plz_data['zipcode'] == plz, [
        'latitude', 'longitude']].iloc[0].tolist()

def calculateMinimumDistanceToNextWeatherStation(weatherfiles_stations):
    weatherfiles_stations['distance'] = weatherfiles_stations.apply(lambda x: geodesic((x['latitude'], x['longitude']),
                                                                                           (x['latitude_building'], x['longitude_building'])).km, axis=1)

def getFilenameWithMinimumDistance(weatherfiles_stations):
    return weatherfiles_stations.loc[weatherfiles_stations['distance'].idxmin(
    ), 'filename']

def getCoordinatesStation(weatherfiles_stations):
    return weatherfiles_stations.loc[weatherfiles_stations['distance'].idxmin(), [
            'latitude', 'longitude']].tolist()

def getDistance(weatherfiles_stations):
    return weatherfiles_stations.loc[weatherfiles_stations['distance'].idxmin(
    ), 'distance']
