from data_source.datasource_csv import DataSourceCSV
from utils.location_utils import *
import sys
import os
import math
import datetime

mainPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, mainPath)


class Location:
    def __init__(self):
        self.datasourcecsv = DataSourceCSV()

    def getWeatherDataObjects(self, weather_period, file_name):
        return (
            self.datasourcecsv.getWeatherData(
                os.path.join(
                    mainPath,
                    f'auxiliary/weather_data/weather_data_TMYx_2007_2021{file_name}',
                )
            )
            if weather_period == "2007-2021"
            else self.datasourcecsv.getWeatherData(
                os.path.join(mainPath, f'auxiliary/weather_data/{file_name}')
            )
        )

    def getEPWFile(self, plz, weather_period):
        return self.datasourcecsv.getEPWFile(plz, weather_period)

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
        latitude_rad, longitude_rad = getRadians(latitude_deg, longitude_deg)

        # Set the date in UTC based off the hour of year and the year itself
        start_of_year, utc_datetime, day_of_year = calcStartDayOfYearAndUTC(
            year, hoy)

        # Calculate the declination angle: The variation due to the earths tilt
        # http://www.pveducation.org/pvcdrom/properties-of-sunlight/declination-angle
        declination_rad, angle_of_day, equation_of_time = calcDeclinationAndAngleOfDayAndEquationOfTime(
            day_of_year)

        # Normalise the day to 2*pi
        # There is some reason as to why it is 364 and not 365.26

        # The deviation between local standard time and true solar time

        # True Solar Time
        solar_time, hour_angle_rad = calcSolarTImeAndHourAngle(
            utc_datetime, longitude_deg, equation_of_time, solar_time)

        # Angle between the local longitude and longitude where the sun is at
        # higher altitude

        # Altitude Position of the Sun in Radians
        altitude_rad = calcAltitudeRad(
            latitude_rad, declination_rad, hour_angle_rad)

        # Azimuth Position fo the sun in radians
        azimuth_rad = calcAzimuthRad(
            declination_rad, hour_angle_rad, altitude_rad)

        # I don't really know what this code does, it has been imported from
        # PySolar
        if (math.cos(hour_angle_rad) >= (math.tan(declination_rad) / math.tan(latitude_rad))):
            return math.degrees(altitude_rad), math.degrees(azimuth_rad)
        else:
            return math.degrees(altitude_rad), (180 - math.degrees(azimuth_rad))
