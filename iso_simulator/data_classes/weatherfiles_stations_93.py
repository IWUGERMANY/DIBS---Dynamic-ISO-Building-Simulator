class WeatherStation93:

    def __init__(self,
                 city: str,
                 state_prov: str,
                 data_type: str,
                 wmo_code: int,
                 latitude: float,
                 longitude: float,
                 altitude: float,
                 jan: int,
                 feb: int,
                 mar: int,
                 apr: int,
                 may: int,
                 jun: int,
                 jul: int,
                 aug: int,
                 sept: int,
                 oct: int,
                 nov: int,
                 dec: int,
                 min: int,
                 max: int,
                 filename: str
                 ):

        self.city = city
        self.state_prov = state_prov
        self.data_type = data_type
        self.wmo_code = wmo_code
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.jan = jan
        self.feb = feb
        self.mar = mar
        self.apr = apr
        self.may = may
        self.jun = jun
        self.jul = jul
        self.aug = aug
        self.sept = sept
        self.oct = oct
        self.nov = nov
        self.dec = dec
        self.min = min
        self.max = max
        self.filename = filename
