class WeatherStation109:

    def __init__(self,
                 city: str,
                 state_prov: str,
                 data_type: str,
                 wmo_code: int,
                 latitude: float,
                 longitude: float,
                 altitude: float,
                 filename: str
                 ):

        self.city = city
        self.state_prov = state_prov
        self.data_type = data_type
        self.wmo_code = wmo_code
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.filename = filename
