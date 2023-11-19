import os
import sys
mainPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, mainPath)
import supply_system, emission_system


class Building:
    def __init__(self,
                 scr_gebaeude_id: str,
                 plz: str,
                 hk_geb: str,
                 uk_geb: str,
                 max_occupancy: int,
                 wall_area_og: float,
                 wall_area_ug: float,
                 window_area_north: float,
                 window_area_east: float,
                 window_area_south: float,
                 window_area_west: float,
                 roof_area: float,
                 net_room_area: float,
                 energy_ref_area: float,
                 base_area: float,
                 gross_base_area: float,
                 building_height: float,
                 net_volume: float,
                 gross_volume: float,
                 envelope_area: float,
                 lighting_load: float,
                 lighting_control: int,
                 lighting_utilisation_factor: float,
                 lighting_maintenance_factor: float,
                 aw_construction: int,
                 shading_device: int,
                 shading_solar_transmittance: float,
                 glass_solar_transmittance: float,
                 glass_solar_shading_transmittance: float,
                 glass_light_transmittance: float,
                 u_windows: float,
                 u_walls: float,
                 u_roof: float,
                 u_base: float,
                 temp_adj_base: float,
                 temp_adj_walls_ug: float,
                 ach_inf: float,
                 ach_win: float,
                 ach_vent: float,
                 heat_recovery_efficiency: int,
                 thermal_capacitance: int,
                 t_set_heating: int,
                 t_start: int,
                 t_set_cooling: int,
                 night_flushing_flow: int,
                 max_heating_energy_per_floor_area: float,
                 max_cooling_energy_per_floor_area: float,
                 heating_supply_system: str,
                 cooling_supply_system: str,
                 heating_emission_system: str,
                 cooling_emission_system: str,
                 dhw_system):

        self.scr_gebaeude_id = scr_gebaeude_id
        self.plz = plz
        self.hk_geb = hk_geb
        self.uk_geb = uk_geb
        self.max_occupancy = max_occupancy
        self.wall_area_og = wall_area_og
        self.wall_area_ug = wall_area_ug
        self.window_area_north = window_area_north
        self.window_area_east = window_area_east
        self.window_area_east = window_area_east
        self.window_area_south = window_area_south
        self.window_area_west = window_area_west
        self.roof_area = roof_area
        self.net_room_area = net_room_area
        self.energy_ref_area = energy_ref_area
        self.base_area = base_area
        self.gross_base_area = gross_base_area
        self.building_height = building_height
        self.net_volume = net_volume
        self.gross_volume = gross_volume
        self.envelope_area = envelope_area
        self.lighting_load = lighting_load
        self.lighting_control = lighting_control
        self.lighting_utilisation_factor = lighting_utilisation_factor
        self.lighting_maintenance_factor = lighting_maintenance_factor
        self.aw_construction = aw_construction
        self.shading_device = shading_device
        self.shading_solar_transmittance = shading_solar_transmittance
        self.glass_solar_transmittance = glass_solar_transmittance
        self.glass_solar_shading_transmittance = glass_solar_shading_transmittance
        self.glass_light_transmittance = glass_light_transmittance
        self.u_windows = u_windows
        self.u_walls = u_walls
        self.u_roof = u_roof
        self.u_base = u_base
        self.temp_adj_base = temp_adj_base
        self.temp_adj_walls_ug = temp_adj_walls_ug
        self.ach_inf = ach_inf
        self.ach_win = ach_win
        self.ach_vent = ach_vent
        self.heat_recovery_efficiency = heat_recovery_efficiency
        self.thermal_capacitance = thermal_capacitance
        self.t_set_heating = t_set_heating
        self.t_start = t_start
        self.t_set_cooling = t_set_cooling
        self.night_flushing_flow = night_flushing_flow
        self.max_heating_energy_per_floor_area = max_heating_energy_per_floor_area
        self.max_cooling_energy_per_floor_area = max_cooling_energy_per_floor_area
        self.heating_supply_system = getattr(supply_system, heating_supply_system)
        self.cooling_supply_system = getattr(supply_system, cooling_supply_system)
        self.heating_emission_system = getattr(emission_system, heating_emission_system)
        self.cooling_emission_system = getattr(emission_system, cooling_emission_system)
        self.dhw_system = dhw_system
