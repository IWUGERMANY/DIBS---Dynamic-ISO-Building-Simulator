
"""
Heating load according to DIN 12831-1 chapter 8, simplified calculation
Author: GB
25.01.2024
"""

class HeatingLoadCalculator:
    def heating_load(self,
                     u_windows,
                     u_walls,
                     u_roof,
                     u_base,
                     temp_adj_base,
                     temp_adj_walls_ug,
                     wall_area_og,
                     wall_area_ug,
                     window_area_north,
                     window_area_east,
                     window_area_south,
                     window_area_west,
                     roof_area,
                     base_area,
                     t_set_heating,
                     thermal_bridges_supplement,  # introduced for this class
                     room_vol, # in documentation but not in building_physics.py
                     year_of_construction, # introduced for this class
                     norm_exterior_temperature):

        # Area of all windows
        # [m2]
        self.window_area_north = window_area_north
        self.window_area_east = window_area_east
        self.window_area_south = window_area_south
        self.window_area_west = window_area_west
        self.window_area = window_area_north + window_area_east + window_area_south + window_area_west

        # Set air change rate according to norm
        # [h-1]
        if year_of_construction >= 1995:
            self.ach_norm = 0.25
        elif year_of_construction < 1995 \
                and year_of_construction >= 1977:
            self.ach_norm = 0.5
        elif year_of_construction < 1977:
            self.ach_norm = 1

        # Conductance of opaque surfaces to exterior, including heat bridges
        # [W/K]
        self.h_tr_op_hb = ((u_walls + thermal_bridges_supplement) * wall_area_og) + \
                          ((u_roof + thermal_bridges_supplement) * roof_area) + \
                          ((u_base + thermal_bridges_supplement) * base_area * temp_adj_base) + \
                          ((u_walls + thermal_bridges_supplement) * wall_area_ug * temp_adj_walls_ug)

        # Conductance to exterior through windows
        # [W/K]
        self.h_tr_w = (u_windows + thermal_bridges_supplement) * self.window_area

        # Total heat transmission losses
        # [W]
        self.phi_t = (self.h_tr_op_hb + self.h_tr_w) * (t_set_heating - norm_exterior_temperature)

        # Ventilation losses
        # [W]
        self.phi_v = room_vol * self.ach_norm * 0.34 * (t_set_heating - norm_exterior_temperature) # 0.34 is the air constant

        # Heating load
        # [W]
        self.phi_hl = self.phi_t + self.phi_v

###########################################################################
# Exemplary calculations
###########################################################################

# Instantiate an object of the class
heating_load_calculator = HeatingLoadCalculator()

# # Example ZUB Helena EFH_GEG
# u_windows = 0.85  # U-value of windows [W/(m^2*K)]
# u_walls = 0.15  # U-value of walls [W/(m^2*K)]
# u_roof = 0.11  # U-value of roof [W/(m^2*K)]
# u_base = 0.19  # U-value of base [W/(m^2*K)]
# temp_adj_base = 0.3  # Temperature adjustment factor for the floor - 0.3 for floor against ground, 0.5 for floor against unheated
# temp_adj_walls_ug = 0.3  # Temperature adjustment factor for walls below ground
# wall_area_og = 34.3+28.10+34.7+26.3  # Wall area exposed to outdoor ground [m^2]
# wall_area_ug = 0  # Wall area underground [m^2]
# window_area_north = 5.7  # Window area facing north [m^2]
# window_area_east = 5.8  # Window area facing east [m^2]
# window_area_south = 5.3  # Window area facing south [m^2]
# window_area_west = 9.7  # Window area facing west [m^2]
# roof_area = 77  # Roof area [m^2]
# base_area = 98.7  # Base area [m^2]
# t_set_heating = 20.0  # Set heating temperature [°C]
# thermal_bridges_supplement = 0.1  # Additional thermal bridges supplement [W/(m^2*K)]
# room_vol = 465  # Room volume [m^3]
# year_of_construction = 2005  # Year of construction
# norm_exterior_temperature = -10.0  # Norm exterior temperature [°C]


# Beispiel ZUB Helena WP Hessen
u_windows = 1.3  # U-value of windows [W/(m^2*K)]
u_walls = 0.2  # U-value of walls [W/(m^2*K)]
u_roof = 0.14 # U-value of roof [W/(m^2*K)]
u_base = 0.25 # U-value of base [W/(m^2*K)]
temp_adj_base = 0.5  # Temperature adjustment factor for the floor - 0.3 for floor against ground, 0.5 for floor against unheated
temp_adj_walls_ug = 0.3  # Temperature adjustment factor for walls below ground
wall_area_og = 139  # Wall area exposed to outdoor ground [m^2]
wall_area_ug = 0  # Wall area underground [m^2]
window_area_north = 16.95+6.18+3.96+2.1  # Window area facing north [m^2]
window_area_east = 0  # Window area facing east [m^2]
window_area_south = 0  # Window area facing south [m^2]
window_area_west = 0  # Window area facing west [m^2]
roof_area = 148.9  # Roof area [m^2]
base_area = 115.8  # Base area [m^2]
t_set_heating = 20.0  # Set heating temperature [°C]
thermal_bridges_supplement = 0  # Additional thermal bridges supplement [W/(m^2*K)]
room_vol = 553  # Room volume [m^3]
year_of_construction = 2023  # Year of construction
norm_exterior_temperature = -10.0  # Norm exterior temperature [°C]

# Call the heating_load method with the provided parameters
heating_load_calculator.heating_load(u_windows, u_walls, u_roof, u_base, temp_adj_base,
                                temp_adj_walls_ug, wall_area_og, wall_area_ug,
                                window_area_north, window_area_east, window_area_south,
                                window_area_west, roof_area, base_area, t_set_heating,
                                thermal_bridges_supplement, room_vol, year_of_construction,
                                norm_exterior_temperature)

calculated_heating_load = heating_load_calculator.phi_hl
calculated_transmission_losses = heating_load_calculator.phi_t /(t_set_heating - norm_exterior_temperature)
calculated_ventilation_losses = heating_load_calculator.phi_v /(t_set_heating - norm_exterior_temperature)

print("Calculated Heating Load [W]:", round(calculated_heating_load))
print("Calculated Transmission Losses [W/K]:", round(calculated_transmission_losses))
print("Calculated Ventilation Losses [W/K]:", round(calculated_ventilation_losses))
print("ach_norm [h-1]: ", heating_load_calculator.ach_norm)



