import math

class Window:

    def __init__(self, azimuth_tilt, alititude_tilt = 90, 
                 glass_solar_transmittance = 0.7,
                 glass_solar_shading_transmittance = 0.2,
                 glass_light_transmittance = 0.8, 
                 area = 1):
    
        self.alititude_tilt_rad = math.radians(alititude_tilt)
        self.azimuth_tilt_rad = math.radians(azimuth_tilt)
        self.glass_solar_transmittance = glass_solar_transmittance
        self.glass_light_transmittance = glass_light_transmittance
        self.area = area
        self.glass_solar_shading_transmittance = glass_solar_shading_transmittance
    
