
__author__ = "Wail Samjouni"
__copyright__ = "Copyright 2023, Institut Wohnen und Umwelt"
__license__ = "MIT"

class PLZData:

    """
    Sets the parameters of the PLZData.

    Args: 
        country_code: The country code
        zipcode: The zipcode
        place: The place
        state: The state
        state_code: The state code
        province: The province
        province_code: The province code
        community: The community
        community_code: The community code
        latitude: The latitude
        longitude: The longitude

    """

    def __init__(self,
                country_code,
                zipcode,
                place,
                state,
                state_code,
                province,
                province_code,
                community,
                community_code,
                latitude: float,
                longitude: float
                 ):
        self.country_code = country_code,
        self.zipcode = zipcode,
        self.place = place,
        self.state = state,
        self.state_code = state_code,
        self.province = province,
        self.province_code = province_code,
        self.community = community,
        self.community_code = community_code,
        self.latitude = latitude,
        self.longitude = longitude
