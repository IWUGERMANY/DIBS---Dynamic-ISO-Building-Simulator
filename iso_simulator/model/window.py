import math


class Window:
    def __init__(
        self,
        azimuth_tilt,
        alititude_tilt=90,
        glass_solar_transmittance=0.7,
        glass_solar_shading_transmittance=0.2,
        glass_light_transmittance=0.8,
        area=1,
    ):
        self.alititude_tilt_rad = math.radians(alititude_tilt)
        self.azimuth_tilt_rad = math.radians(azimuth_tilt)
        self.glass_solar_transmittance = glass_solar_transmittance
        self.glass_light_transmittance = glass_light_transmittance
        self.area = area
        self.glass_solar_shading_transmittance = glass_solar_shading_transmittance

    def calc_solar_gains(
        self,
        sun_altitude: float,
        sun_azimuth: float,
        normal_direct_radiation: int,
        horizontal_diffuse_radiation: int,
        t_air: float,
        hour: int,
    ) -> None:
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
        # Assume cooling season from 01/04 9am - 01/10 9am
        cooling_season = 2169 < hour < 6561

        self.set_variable_for_calc_sun(
            sun_altitude,
            sun_azimuth,
            normal_direct_radiation,
            horizontal_diffuse_radiation,
        )
        if (
            t_air > 24 and cooling_season and self.glass_solar_shading_transmittance > 0
        ):  # Check if the building has sunshading
            self.solar_gains = (
                self.glass_solar_shading_transmittance * self.incident_solar
            )

        else:
            self.solar_gains = self.glass_solar_transmittance * self.incident_solar

    def set_variable_for_calc_sun(
        self,
        sun_altitude: float,
        sun_azimuth: float,
        normal_direct_radiation: int,
        horizontal_diffuse_radiation: int,
    ) -> None:
        direct_factor = self.calc_direct_solar_factor(
            sun_altitude,
            sun_azimuth,
        )
        diffuse_factor = self.calc_diffuse_solar_factor()

        direct_solar = direct_factor * normal_direct_radiation
        diffuse_solar = horizontal_diffuse_radiation * diffuse_factor
        self.incident_solar = (direct_solar + diffuse_solar) * self.area

    def calc_diffuse_solar_factor(self) -> float:
        """
        Calculates the proportion of diffuse radiation
        """
        # Proportion of incident light on the window surface
        return (1 + math.cos(self.alititude_tilt_rad)) / 2

    def calc_illuminance(
        self,
        sun_altitude: float,
        sun_azimuth: float,
        normal_direct_illuminance: int,
        horizontal_diffuse_illuminance: int,
    ) -> None:
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

        direct_factor = self.calc_direct_solar_factor(
            sun_altitude,
            sun_azimuth,
        )
        diffuse_factor = self.calc_diffuse_solar_factor()

        direct_illuminance = direct_factor * normal_direct_illuminance
        diffuse_illuminance = diffuse_factor * horizontal_diffuse_illuminance

        self.incident_illuminance = (
            direct_illuminance + diffuse_illuminance
        ) * self.area
        self.transmitted_illuminance = (
            self.incident_illuminance * self.glass_light_transmittance
        )

    def calc_direct_solar_factor(
        self, sun_altitude: float, sun_azimuth: float
    ) -> float:
        """
        Calculates the cosine of the angle of incidence on the window
        """
        sun_altitude_rad = math.radians(sun_altitude)
        sun_azimuth_rad = math.radians(sun_azimuth)

        # Proportion of the radiation incident on the window (cos of the
        # incident ray)
        # ref:Quaschning, Volker, and Rolf Hanitsch. "Shade calculations in photovoltaic systems." ISES Solar World Conference, Harare. 1995.
        direct_factor = math.cos(sun_altitude_rad) * math.sin(
            self.alititude_tilt_rad
        ) * math.cos(sun_azimuth_rad - self.azimuth_tilt_rad) + math.sin(
            sun_altitude_rad
        ) * math.cos(
            self.alititude_tilt_rad
        )

        # If the sun is in front of the window surface
        if math.degrees(math.acos(direct_factor)) > 90:
            direct_factor = 0

        return direct_factor
