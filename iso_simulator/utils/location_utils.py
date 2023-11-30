import datetime
import math


def get_radians(latitude_deg, longitude_deg):
    return math.radians(latitude_deg), math.radians(longitude_deg)


def set_utc_date_time(start_of_year, hoy):
    return start_of_year + datetime.timedelta(hours=hoy)


def set_day_of_year(utc_datetime):
    return utc_datetime.timetuple().tm_yday


def calc_start_day_of_year_and_utc(year, hoy):
    start_of_year = datetime.datetime(year, 1, 1, 0, 0, 0, 0)
    utc_datetime = set_utc_date_time(start_of_year, hoy)
    day_of_year = set_day_of_year(utc_datetime)
    return start_of_year, utc_datetime, day_of_year


def calc_declination_rad(day_of_year):
    return math.radians(
        23.45 * math.sin((2 * math.pi / 365.0) * (day_of_year - 81)))


def calc_angle_of_day(day_of_year):
    return (day_of_year - 81) * (2 * math.pi / 364)


def calc_declination_and_angle_of_day(day_of_year):
    return calc_declination_rad(day_of_year), calc_angle_of_day(day_of_year)


def calc_equation_of_time(angle_of_day):
    return (9.87 * math.sin(2 * angle_of_day)) - \
        (7.53 * math.cos(angle_of_day)) - (1.5 * math.sin(angle_of_day))


def calc_solar_time(utc_datetime, longitude_deg, equation_of_time):
    return ((utc_datetime.hour * 60) + utc_datetime.minute +
            (4 * longitude_deg) + equation_of_time) / 60.0


def calc_hour_angle_rad(solar_time):
    return math.radians(15 * (12 - solar_time))


def calc_solar_time_and_hour_angle(utc_datetime, longitude_deg, equation_of_time, solar_time):
    return calc_solar_time(utc_datetime, longitude_deg, equation_of_time), calc_hour_angle_rad(solar_time)


def calc_altitude_rad(latitude_rad, declination_rad, hour_angle_rad):
    return math.asin(math.cos(latitude_rad) * math.cos(declination_rad) * math.cos(hour_angle_rad) +
                     math.sin(latitude_rad) * math.sin(declination_rad))


def calc_azimuth_rad(declination_rad, hour_angle_rad, altitude_rad):
    return math.asin(
        math.cos(declination_rad) * math.sin(hour_angle_rad) / math.cos(altitude_rad))