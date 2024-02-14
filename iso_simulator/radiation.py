"""
Module includes methods to calculate sun position, solar gains, illuminance and determine the nearest weather station of a building.


Portions of this software are copyright of their respective authors and released under the MIT license:
RC_BuildingSimulator, Copyright 2016 Architecture and Building Systems, ETH Zurich

author: "Simon Knoll, Julian Bischof, Michael Hörner "
copyright: "Copyright 2022, Institut Wohnen und Umwelt"
license: "MIT"

"""
__author__ = "Simon Knoll, Julian Bischof, Michael Hörner "
__copyright__ = "Copyright 2022, Institut Wohnen und Umwelt"
__license__ = "MIT"

import numpy as np
import pandas as pd
import os
import sys
import math
import datetime
from geopy.distance import geodesic


class Location(object):
    """
    Set the Location of the Simulation with an Energy Plus Weather File
    
    Methods:
        getEPWFile: Function finds the epw file depending on building location
        calc_sun_position: Calculates the sun position for a specific hour and location
    """

    def __init__(self, epwfile_path):

        # Set EPW Labels and import epw file
        epw_labels = ['year', 'month', 'day', 'hour', 'minute', 'datasource', 'drybulb_C', 'dewpoint_C',
                      'relhum_percent',
                      'atmos_Pa', 'exthorrad_Whm2', 'extdirrad_Whm2', 'horirsky_Whm2', 'glohorrad_Whm2',
                      'dirnorrad_Whm2', 'difhorrad_Whm2', 'glohorillum_lux', 'dirnorillum_lux', 'difhorillum_lux',
                      'zenlum_lux', 'winddir_deg', 'windspd_ms', 'totskycvr_tenths', 'opaqskycvr_tenths',
                      'visibility_km',
                      'ceiling_hgt_m', 'presweathobs', 'presweathcodes', 'precip_wtr_mm', 'aerosol_opt_thousandths',
                      'snowdepth_cm', 'days_last_snow', 'Albedo', 'liq_precip_depth_mm', 'liq_precip_rate_Hour']

        # Import EPW file
        self.weather_data = pd.read_csv(
            epwfile_path, skiprows=8, header=None, names=epw_labels).drop('datasource', axis=1)

    def getEPWFile(plz, weather_period):
        """
        Function finds the epw file depending on building location
        

        :external input data: File with german zip codes [../auxiliary/weather_data/plzcodes.csv]
                              File with metadata of weather stations (e.g. longitude, latitude) [../auxiliary/weather_data/weatherfiles_stations_93.csv]
        
        :return epw_filename: filename of the epw
        :rtype: tuple (string)
        :return coordinates_station: latitude and longitute of the selected station
        :rtype: tuple (float)
        """

        # Read data
        # plz_data = pd.read_csv(os.path.join('../auxiliary/weather_data/plzcodes.csv'), encoding = 'latin')
        plz_data = pd.read_csv(os.path.join('../auxiliary/weather_data/plzcodes.csv'), encoding='latin',
                               dtype={'zipcode': int})

        if (weather_period == "2007-2021"):
            weatherfiles_stations = pd.read_csv(
                os.path.join('../auxiliary/weather_data/weather_data_TMYx_2007_2021/weatherfiles_stations_109.csv'),
                sep=';')
        else:
            weatherfiles_stations = pd.read_csv(os.path.join('../auxiliary/weather_data/weatherfiles_stations_93.csv'),
                                                sep=';')

        # Pick latitude and longitude from plz_data and put values into a list
        coordinates_plz = plz_data.loc[plz_data['zipcode'] == plz, ['latitude', 'longitude']].iloc[0].tolist()

        # Append plz to weatherfiles_stations
        weatherfiles_stations['latitude_building'] = coordinates_plz[0]
        weatherfiles_stations['longitude_building'] = coordinates_plz[1]

        # Calculate minimum distance to next weather station
        weatherfiles_stations['distance'] = weatherfiles_stations.apply(
            lambda x: geodesic((x['latitude'], x['longitude']),
                               (x['latitude_building'], x['longitude_building'])).km, axis=1)

        # Pick filename of minimum distance
        epw_filename = weatherfiles_stations.loc[weatherfiles_stations['distance'].idxmin(), 'filename']

        # Pick latitude and longitude from station as arguments in calc_sun_position(), See annualSimulation.py
        coordinates_station = weatherfiles_stations.loc[
            weatherfiles_stations['distance'].idxmin(), ['latitude', 'longitude']].tolist()

        # Distance 
        distance = distance = weatherfiles_stations.loc[weatherfiles_stations['distance'].idxmin(), 'distance']

        return epw_filename, coordinates_station, distance

    def calc_sun_position(self, latitude_deg, longitude_deg, year, hoy):
        """
        Calculates the sun position for a specific hour and location

        :param latitude_deg: Geographical Latitude in Degrees
        :type latitude_deg: float
        :param longitude_deg: Geographical Longitude in Degrees
        :type longitude_deg: float
        :param year: year
        :type year: int
        :param hoy: Hour of the year from the start. The first hour of January is 1
        :type hoy: int
        :return: altitude, azimuth: Sun position in altitude and azimuth degrees [degrees]
        :rtype: tuple
        """

        # Convert to Radians
        latitude_rad = math.radians(latitude_deg)
        longitude_rad = math.radians(longitude_deg)

        # Set the date in UTC based off the hour of year and the year itself
        start_of_year = datetime.datetime(year, 1, 1, 0, 0, 0, 0)
        utc_datetime = start_of_year + datetime.timedelta(hours=hoy)

        # Angular distance of the sun north or south of the earths equator
        # Determine the day of the year.
        day_of_year = utc_datetime.timetuple().tm_yday

        # Calculate the declination angle: The variation due to the earths tilt
        # http://www.pveducation.org/pvcdrom/properties-of-sunlight/declination-angle
        declination_rad = math.radians(
            23.45 * math.sin((2 * math.pi / 365.0) * (day_of_year - 81)))

        # Normalise the day to 2*pi
        # There is some reason as to why it is 364 and not 365.26
        angle_of_day = (day_of_year - 81) * (2 * math.pi / 364)

        # The deviation between local standard time and true solar time
        equation_of_time = (9.87 * math.sin(2 * angle_of_day)) - \
                           (7.53 * math.cos(angle_of_day)) - (1.5 * math.sin(angle_of_day))

        # True Solar Time
        solar_time = ((utc_datetime.hour * 60) + utc_datetime.minute +
                      (4 * longitude_deg) + equation_of_time) / 60.0

        # Angle between the local longitude and longitude where the sun is at
        # higher altitude
        hour_angle_rad = math.radians(15 * (12 - solar_time))

        # Altitude Position of the Sun in Radians
        altitude_rad = math.asin(math.cos(latitude_rad) * math.cos(declination_rad) * math.cos(hour_angle_rad) +
                                 math.sin(latitude_rad) * math.sin(declination_rad))

        # Azimuth Position fo the sun in radians
        azimuth_rad = math.asin(
            math.cos(declination_rad) * math.sin(hour_angle_rad) / math.cos(altitude_rad))

        # I don't really know what this code does, it has been imported from
        # PySolar
        if (math.cos(hour_angle_rad) >= (math.tan(declination_rad) / math.tan(latitude_rad))):
            return math.degrees(altitude_rad), math.degrees(azimuth_rad)
        else:
            return math.degrees(altitude_rad), (180 - math.degrees(azimuth_rad))


class Window(object):
    """
    Methods:
        calc_solar_gains: Calculates the solar gains in the building zone through the set window
        calc_illuminance: Calculates the illuminance in the building zone through the set window
        calc_direct_solar_factor: Calculates the cosine of the angle of incidence on the window 
        calc_diffuse_solar_factor: Calculates the proportion of diffuse radiation
    """

    def __init__(self, azimuth_tilt, alititude_tilt=90,
                 glass_solar_transmittance=0.7,
                 glass_solar_shading_transmittance=0.2,
                 glass_light_transmittance=0.8,
                 area=1):

        self.alititude_tilt_rad = math.radians(alititude_tilt)
        self.azimuth_tilt_rad = math.radians(azimuth_tilt)
        self.glass_solar_transmittance = glass_solar_transmittance
        self.glass_light_transmittance = glass_light_transmittance
        self.area = area
        self.glass_solar_shading_transmittance = glass_solar_shading_transmittance

    def calc_solar_gains(self, sun_altitude, sun_azimuth, normal_direct_radiation, horizontal_diffuse_radiation, t_air,
                         hour):
        """
        Calculates the solar gains in the building zone through the set window

        :param sun_altitude: Altitude Angle of the Sun in Degrees
        :type sun_altitude: float
        :param sun_azimuth: Azimuth angle of the sun in degrees
        :type sun_azimuth: float
        :param normal_direct_radiation: Normal Direct Radiation from weather file
        :type normal_direct_radiation: float
        :param horizontal_diffuse_radiation: Horizontal Diffuse Radiation from weather file
        :type horizontal_diffuse_radiation: float
        
        # Added:
        #param t_out: Outdoor temperature from weather file
        :type t_out: float
        
        :return: self.incident_solar, Incident Solar Radiation on window
        :return: self.solar_gains - Solar gains in building after transmitting through the window
        :rtype: float
        """

        # Check conditions cooling seasons == True and outdoor temperature > 24 (requiered indoor temperature in the cooling case for 85% of usage zones according to DIN V 18599-10):
        # If condition is true, use reduced glass_solar_transmittance (called glass_solar_shading_transmittance) due to the use
        # of activated sunshadings 
        cooling_season = (2169 < hour < 6561)  # Assume cooling season from 01/04 9am - 01/10 9am

        if round(t_air, 1) > 24 and (cooling_season == True):

            direct_factor = self.calc_direct_solar_factor(sun_altitude, sun_azimuth, )
            diffuse_factor = self.calc_diffuse_solar_factor()

            direct_solar = direct_factor * normal_direct_radiation
            diffuse_solar = horizontal_diffuse_radiation * diffuse_factor
            self.incident_solar = (direct_solar + diffuse_solar) * self.area

            if self.glass_solar_shading_transmittance > 0:  # Check if the building has sunshading

                self.solar_gains = self.glass_solar_shading_transmittance * self.incident_solar

            else:
                self.solar_gains = self.glass_solar_transmittance * self.incident_solar

        else:

            direct_factor = self.calc_direct_solar_factor(sun_altitude, sun_azimuth)
            diffuse_factor = self.calc_diffuse_solar_factor()

            direct_solar = direct_factor * normal_direct_radiation
            diffuse_solar = horizontal_diffuse_radiation * diffuse_factor
            self.incident_solar = (direct_solar + diffuse_solar) * self.area

            self.solar_gains = self.glass_solar_transmittance * self.incident_solar

    def calc_illuminance(self, sun_altitude, sun_azimuth, normal_direct_illuminance, horizontal_diffuse_illuminance):
        """
        Calculates the illuminance in the building zone through the set window

        :param sun_altitude: Altitude Angle of the Sun in Degrees
        :type sun_altitude: float
        :param sun_azimuth: Azimuth angle of the sun in degrees
        :type sun_azimuth: float
        :param normal_direct_illuminance: Normal Direct Illuminance from weather file [Lx]
        :type normal_direct_illuminance: float
        :param horizontal_diffuse_illuminance: Horizontal Diffuse Illuminance from weather file [Lx]
        :type horizontal_diffuse_illuminance: float
        :return: self.incident_illuminance, Incident Illuminance on window [Lumens]
        :return: self.transmitted_illuminance - Illuminance in building after transmitting through the window [Lumens]
        :rtype: float
        """

        direct_factor = self.calc_direct_solar_factor(sun_altitude, sun_azimuth, )
        diffuse_factor = self.calc_diffuse_solar_factor()

        direct_illuminance = direct_factor * normal_direct_illuminance
        diffuse_illuminance = diffuse_factor * horizontal_diffuse_illuminance

        self.incident_illuminance = (
                                            direct_illuminance + diffuse_illuminance) * self.area
        self.transmitted_illuminance = self.incident_illuminance * \
                                       self.glass_light_transmittance

    def calc_direct_solar_factor(self, sun_altitude, sun_azimuth):
        """
        Calculates the cosine of the angle of incidence on the window 
        """
        sun_altitude_rad = math.radians(sun_altitude)
        sun_azimuth_rad = math.radians(sun_azimuth)

        # Proportion of the radiation incident on the window (cos of the
        # incident ray)
        # ref:Quaschning, Volker, and Rolf Hanitsch. "Shade calculations in photovoltaic systems." ISES Solar World Conference, Harare. 1995.
        direct_factor = math.cos(sun_altitude_rad) * math.sin(self.alititude_tilt_rad) * math.cos(
            sun_azimuth_rad - self.azimuth_tilt_rad) + \
                        math.sin(sun_altitude_rad) * math.cos(self.alititude_tilt_rad)

        # If the sun is in front of the window surface
        if (math.degrees(math.acos(direct_factor)) > 90):
            direct_factor = 0

        else:
            pass

        return direct_factor

    def calc_diffuse_solar_factor(self):
        """
        Calculates the proportion of diffuse radiation
        """
        # Proportion of incident light on the window surface
        return (1 + math.cos(self.alititude_tilt_rad)) / 2


if __name__ == '__main__':
    pass
