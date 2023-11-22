import datetime
import math


def getRadians(latitude_deg, longitude_deg):
    return math.radians(latitude_deg), math.radians(longitude_deg)


def setUtcDateTime(start_of_year, hoy):
    return start_of_year + datetime.timedelta(hours=hoy)


def setDayOfYear(utc_datetime):
    return utc_datetime.timetuple().tm_yday


def calcStartDayOfYearAndUTC(year, hoy):
    start_of_year = datetime.datetime(year, 1, 1, 0, 0, 0, 0)
    utc_datetime = setUtcDateTime(start_of_year, hoy)
    day_of_year = setDayOfYear(utc_datetime)
    return start_of_year, utc_datetime, day_of_year


def calcDeclinationRad(day_of_year):
    return math.radians(
        23.45 * math.sin((2 * math.pi / 365.0) * (day_of_year - 81)))


def calcAngleOfDay(day_of_year):
    return (day_of_year - 81) * (2 * math.pi / 364)


def calcDeclinationAndAngleOfDayAndEquationOfTime(day_of_year, angle_of_day):
    return calcDeclinationRad(day_of_year), calcAngleOfDay(day_of_year), calcEquationOfTime(angle_of_day)


def calcEquationOfTime(angle_of_day):
    return (9.87 * math.sin(2 * angle_of_day)) - \
        (7.53 * math.cos(angle_of_day)) - (1.5 * math.sin(angle_of_day))


def calcSolartime(utc_datetime, longitude_deg, equation_of_time):
    return ((utc_datetime.hour * 60) + utc_datetime.minute +
            (4 * longitude_deg) + equation_of_time) / 60.0


def calcHourAngleRad(solar_time):
    return math.radians(15 * (12 - solar_time))


def calcSolarTImeAndHourAngle(utc_datetime, longitude_deg, equation_of_time, solar_time):
    return calcSolartime(utc_datetime, longitude_deg, equation_of_time), calcHourAngleRad(solar_time)


def calcAltitudeRad(latitude_rad, declination_rad, hour_angle_rad):
    return math.asin(math.cos(latitude_rad) * math.cos(declination_rad) * math.cos(hour_angle_rad) +
                     math.sin(latitude_rad) * math.sin(declination_rad))


def calcAzimuthRad(declination_rad, hour_angle_rad, altitude_rad):
    return math.asin(
        math.cos(declination_rad) * math.sin(hour_angle_rad) / math.cos(altitude_rad))
