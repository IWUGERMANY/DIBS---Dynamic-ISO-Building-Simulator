class ZipCode:

    def __init__(self,
                 country_code: str,
                 zipcode: str,
                 place: str,
                 state: str,
                 state_code: str,
                 province: str,
                 province_code: int,
                 community: str,
                 community_code: int,
                 latitude: float,
                 longitude: float
                 ):

        self.country_code = country_code
        self.zipcode = zipcode
        self.place = place
        self.state = state
        self.state_code = state_code
        self.province = province
        self.province_code = province_code
        self.community = community
        self.community_code = community_code
        self.latitude = latitude
        self.longitude = longitude
