"""
Physics required to calculate sensible space heating and space cooling loads, and space lighting loads (DIN EN ISO 13970:2008)

The equations presented here is this code are derived from ISO 13790 Annex C, Methods are listed in order of apperance in the Annex 


Portions of this software are copyright of their respective authors and released under the MIT license:
RC_BuildingSimulator, Copyright 2016 Architecture and Building Systems, ETH Zurich

author: "Julian Bischof, Simon Knoll, Michael Hörner "
copyright: "Copyright 2023, Institut Wohnen und Umwelt"
license: "MIT"

"""
__author__ = "Julian Bischof, Simon Knoll, Michael Hörner "
__copyright__ = "Copyright 2023, Institut Wohnen und Umwelt"
__license__ = "MIT"


import supply_system
import emission_system


class Building(object):
    """
    Sets the parameters of the building.
    
    INPUT PARAMETER DEFINITION 
    scr_gebaeude_id: Building Screening-ID
    plz: Zipcode of building location
    hk_geb: Usage type (main category)
    uk_geb: Usage type (subcategory)
    max_occupancy: Max. number of persons 
    wall_area_og: Area of all walls above ground in contact with the outside [m2]
    wall_area_ug: Area of all walls below ground in contact with soil [m2]
    window_area_north: Area of the glazed surface in contact with the outside facing north [m2]
    window_area_east: Area of the glazed surface in contact with the outside facing east [m2]
    window_area_south: Area of the glazed surface in contact with the outside facing south [m2]
    window_area_west: Area of the glazed surface in contact with the outside facing west [m2]
    roof_area: Area of the roof in contact with the outside [m2]
    net_room_area: Area of all floor areas from usable rooms including all floor plan levels of the building (Refers to "Netto-Raumfläche", DIN 277-1:2016-01)
    base_area: Area for the calculation of transmission heat losses to the soil. Also used to calculate the building's volume.
    energy_ref_area: Energy reference area of the building   
    building_height: Mean height of the building [m]
    lighting_load: Lighting Load [W/m2] 
    lighting_control: Lux threshold at which the lights turn on [Lx]
    lighting_utilisation_factor: A factor that determines how much natural solar lumminace is effectively utilised in the space
    lighting_maintenance_factor: A factor based on how dirty the windows area
    glass_solar_transmittance: Solar radiation passing through the window (g-value)
    glass_solar_shading_transmittance: Solar radiation passing through the window with active shading devices
    glass_light_transmittance: Solar illuminance passing through the window
    u_windows: U value of glazed surfaces [W/m2K]
    u_walls: U value of external walls  [W/m2K]
    u_roof: U value of the roof [W/m2K]
    u_base: U value of the floor [W/m2K]
    temp_adj_base: Temperature adjustment factor for the floor 
    temp_adj_walls_ug: Temperature adjustment factor for walls below ground
    ach_inf: Air changes per hour through infiltration [Air Changes Per Hour] 
    ach_win: Air changes per hour through opened windows [Air Changes Per Hour]
    ach_vent: Air changes per hour through ventilation [Air Changes Per Hour]
    ventilation_efficiency: Efficiency of the heat recovery system for ventilation. Set to 0 if there is no heat recovery 
    night_flushing_flow: Air changes per hour through night flushing [Air Changes Per Hour]                                                    
    thermal_capacitance: Thermal capacitance of the building [J/m2K]
    t_set_heating : Thermal heating set point [C]
    t_set_cooling: Thermal cooling set point [C]
    max_cooling_energy_per_floor_area: Maximum cooling load. Set to -np.inf for unrestricted cooling [C]
    max_heating_energy_per_floor_area: Maximum heating load per floor area. Set to no.inf for unrestricted heating [C]
    heating_supply_system: The type of heating system
    cooling_supply_system: The type of cooling system
    heating_emission_system: How the heat is distributed to the building
    cooling_emission_system: How the cooling energy is distributed to the building


    VARIABLE DEFINITION

    internal_gains: Internal Heat Gains [W]
    solar_gains: Solar Heat Gains after transmitting through the window [W]
    t_out: Outdoor air temperature [C]
    t_m_prev: Thermal mass temperature from the previous time step 
    ill: Illuminance transmitting through the window [lumen]
    occupancy: Occupancy [people]

    t_m_next: Medium temperature of the next time step [C]
    t_m: Average between the previous and current time-step of the bulk temperature [C] 

    Inputs to the 5R1C model:
    c_m: Thermal Capacitance of the medium [J/K]
    h_tr_is: Conductance between the air node and the inside surface node [W/K]
    h_tr_w: Heat transfer coefficient from the outside through windows, doors [W/K]
    h_tr_op: Heat transfer coefficient from the outside through opaque elements [W/K]
    h_tr_em: Conductance between outside node and mass node [W/K]
    h_tr_ms: Conductance between mass node and internal surface node [W/K]
    h_ve_adj: Ventilation heat transmission coefficient [W/K]

    phi_m_tot: see formula for the calculation, eq C.5 in standard [W]
    phi_m: Combination of internal and solar gains directly to the medium [W]
    phi_st: combination of internal and solar gains directly to the internal surface [W]
    phi_ia: combination of internal and solar gains to the air [W]
    energy_demand: Heating and Cooling of the Supply air [W]

    h_tr_1: combined heat conductance, see function for definition [W/K]
    h_tr_2: combined heat conductance, see function for definition [W/K]
    h_tr_3: combined heat conductance, see function for definition [W/K]
    """
    
    def __init__(self,
                 scr_gebaeude_id,
                 plz,
                 hk_geb,
                 uk_geb,
                 max_occupancy,
                 wall_area_og,
                 wall_area_ug,
                 window_area_north,
                 window_area_east,
                 window_area_south,
                 window_area_west,
                 roof_area,
                 net_room_area,
                 base_area,
                 energy_ref_area,
                 building_height,
                 lighting_load,
                 lighting_control,
                 lighting_utilisation_factor,
                 lighting_maintenance_factor,
                 glass_solar_transmittance,
                 glass_solar_shading_transmittance,
                 glass_light_transmittance,
                 u_windows,
                 u_walls,
                 u_roof,
                 u_base,
                 temp_adj_base,
                 temp_adj_walls_ug,
                 ach_inf,
                 ach_win,
                 ach_vent,
                 heat_recovery_efficiency,
                 thermal_capacitance,
                 t_start,
                 t_set_heating,
                 t_set_cooling,
                 night_flushing_flow,
                 max_cooling_energy_per_floor_area,
                 max_heating_energy_per_floor_area,
                 heating_supply_system,  
                 cooling_supply_system,
                 heating_emission_system,
                 cooling_emission_system):

        ## Dimensions
        # area of all windows 
        self.window_area_north = window_area_north
        self.window_area_east = window_area_east
        self.window_area_south = window_area_south
        self.window_area_west = window_area_west
        self.window_area = window_area_north + window_area_east + window_area_south + window_area_west  
        # net room area                        
        self.net_room_area = net_room_area   
        # energy reference area
        self.energy_ref_area = energy_ref_area
               
        ## Fenestration and Lighting Properties
        self.glass_solar_transmittance = glass_solar_transmittance
        self.glass_light_transmittance = glass_light_transmittance
        self.glass_solar_shading_transmittance = glass_solar_shading_transmittance
        # lighting load
        self.lighting_load = lighting_load   
        # Lighting set point                       
        self.lighting_control = lighting_control                    
        # How the light entering the window is transmitted to the working plane
        self.lighting_utilisation_factor = lighting_utilisation_factor
        # How dirty the window is. Section 2.2.3.1 Environmental Science Handbook
        self.lighting_maintenance_factor = lighting_maintenance_factor

        ## Constants of the building 
        self.plz = plz
        self.hk_geb = hk_geb
        self.uk_geb = uk_geb
        self.max_occupancy = max_occupancy
        
        # Night flushing
        self.night_flushing_flow = night_flushing_flow

        ## Calculated Properties
        # [m2] Effective mass area (See p. 81, Table 12)
        if thermal_capacitance <= 165000:
            self.mass_area = energy_ref_area * 2.5
            
        elif  165000 < thermal_capacitance <= 260000:
            self.mass_area = energy_ref_area * 3
            
        elif thermal_capacitance > 260000:
            self.mass_area = energy_ref_area * 3.5
            
        # [m3] Calculate building volume
        self.building_vol = base_area * building_height  
        # Calculate internal area (See 7.2.2.2, p. 35/36)  
        self.total_internal_area = energy_ref_area * 4.5
        self.A_t = self.total_internal_area

        # Single Capacitance  5 conductance Model Parameters
        # [kWh/K] Room Capacitance. Default based on ISO standard 12.3.1.2 for medium heavy buildings
        # p. 81, Table 12
        self.c_m = thermal_capacitance * energy_ref_area

        # Conductance of opaque surfaces to exterior [W/K]
        # p. 44, Eq. 18 --> H_x = A_i * U_i
        self.h_tr_op = (u_walls * wall_area_og) + (u_roof * roof_area) + \
                        (base_area * u_base * temp_adj_base) + (wall_area_ug * u_walls * temp_adj_walls_ug)
        # Conductance to exterior through glazed surfaces [W/K], based on
        # U-wert of 1W/m2K
        self.h_tr_w = u_windows * self.window_area
        
        ## Determine the ventilation conductance
        self.ach_inf = ach_inf
        self.ach_win = ach_win
        self.ach_vent = ach_vent
        self.ach_tot = ach_inf + ach_win + ach_vent
        # Total Air Changes Per Hour
        # temperature adjustment factor taking ventilation and infiltration
        # p. 53, Eq. 27
        self.b_ek = (1 - (ach_vent / (self.ach_tot)) * heat_recovery_efficiency)
        # Conductance through ventilation [W/M]
        # transmittance from the internal air to the thermal mass of the building
        # p. 79, Eq. 64    
        self.h_tr_ms = 9.1 * self.mass_area
        # Conductance from the conditioned air to interior building surface
        # p. 35, Eq. 9
        self.h_tr_is = self.total_internal_area * 3.45
        self.h_tr_em = max(0, (1 / ((1/self.h_tr_op) - (1/self.h_tr_ms))))

        ## Thermal set points and starting temperature 
        self.t_set_heating = t_set_heating
        self.t_set_cooling = t_set_cooling
        self.t_start = t_start

        ## Thermal Properties
        # Boolean for if heating is required
        self.has_heating_demand = False  
        # Boolean for if cooling is required
        self.has_cooling_demand = False  
        # max cooling load (W/m2)
        self.max_cooling_energy = max_cooling_energy_per_floor_area * \
            energy_ref_area  
        # max heating load (W/m2)
        self.max_heating_energy = max_heating_energy_per_floor_area * \
            energy_ref_area  

        ## Building System Properties
        self.heating_supply_system = heating_supply_system
        self.cooling_supply_system = cooling_supply_system
        self.heating_emission_system = heating_emission_system
        self.cooling_emission_system = cooling_emission_system
        
        
    @property
    def h_tr_1(self):
        """
        Definition to simplify calc_phi_m_tot
        # (C.6) in [C.3 ISO 13790]
        """
        return 1.0 / (1.0 / self.h_ve_adj + 1.0 / self.h_tr_is)

    @property
    def h_tr_2(self):
        """
        Definition to simplify calc_phi_m_tot
        # (C.7) in [C.3 ISO 13790]
        """
        return self.h_tr_1 + self.h_tr_w

    @property
    def h_tr_3(self):
        """
        Definition to simplify calc_phi_m_tot
        # (C.8) in [C.3 ISO 13790]
        """
        return  1.0 / (1.0 / self.h_tr_2 + 1.0 / self.h_tr_ms)

    @property
    def t_opperative(self):
        """
        The opperative temperature is a weighted average of the air and mean radiant temperatures. 
        It is not used in any further calculation at this stage
        # (C.12) in [C.3 ISO 13790]
        """
        return 0.3 * self.t_air + 0.7 * self.t_s
    
        
    
    
    def calc_h_ve_adj(self, hour, t_out, usage_start, usage_end):     
        """
        Calculates h_ve_adj depending on the building's usage time
        
        # (Eq. 21) in ISO 13790, p. 49-50
        
        :param hour: Hour of the timestep
        :type hour: int
        :param t_out: Outdoor temperature of this timestep
        :type t_out: float
        :param usage_start: Beginning of usage time according to SIA2024
        :type usage_start: int
        :param usage_end: Ending of usage time according to SIA2024
        :type usage_end: int
        
        :return: self.h_ve_adj
        :rtype: float
        """
        # Call this function and check if night flushing needs to be taken into account
        self.check_night_flushing(hour, t_out)
        
        daytime = hour%24
        
        # Check if ach_vent and ach_win is equal to zero (this is necessary due to Eq. C.6, DIN EN ISO 13790)
        if self.ach_vent == 0 and self.ach_win == 0:
            
            self.h_ve_adj = 1200 * 1 * self.building_vol * (self.ach_inf / 3600)
        
        else:    
            if usage_start < usage_end:
                if (usage_start <= daytime < usage_end) == True:
                    if self.night_flushing_on == True:                                           
                        self.h_ve_adj = 1200 * 1 * self.building_vol * (self.night_flushing_flow / 3600)
                    
                        # Set t_set_heating = 0 for the time step, otherwise the heating system heats up during night flushing is on
                        self.t_set_heating = 0
                    
                    else:
                        self.h_ve_adj = 1200 * ((self.b_ek * self.building_vol * (self.ach_vent / 3600)) + (1 * self.building_vol * (self.ach_win / 3600)))
                    
                elif (usage_start <= daytime < usage_end) == False:         
                    if self.night_flushing_on == True:                                    
                        self.h_ve_adj = 1200 * 1 * self.building_vol * (self.night_flushing_flow / 3600)
                    
                        # Set t_set_heating = 0 for the time step, otherwise the heating system heats up during night flushing is on
                        self.t_set_heating = 0
                    
                    else: 
                        # Only infiltration 
                        self.h_ve_adj = 1200 * 1 * self.building_vol * (self.ach_inf / 3600)
                    
                else: 
                     raise ValueError('Something went wrong with ventilation heat loss coefficient h_ve_adj')   
                     
            else:
                if (usage_end <= daytime < usage_start) == False:
                    if self.night_flushing_on == True:
                                
                        self.h_ve_adj = 1200 * 1 * self.building_vol * (self.night_flushing_flow / 3600)
                    
                        # Set t_set_heating = 0 for the time step, otherwise the heating system heats up during night flushing is on
                        self.t_set_heating = 0
                    
                    else:
                        self.h_ve_adj = 1200 * ((self.b_ek * self.building_vol * (self.ach_vent / 3600)) + (1 * self.building_vol * (self.ach_win / 3600)))
                    
                elif (usage_end <= daytime < usage_start) == True:         
                    if self.night_flushing_on == True:                    
                                
                        self.h_ve_adj = 1200 * 1 * self.building_vol * (self.night_flushing_flow / 3600)
                    
                        # Set t_set_heating = 0 for the time step, otherwise the heating system heats up during night flushing is on
                        self.t_set_heating = 0
                    
                    else: 
                        # Only infiltration 
                        self.h_ve_adj = 1200 * 1 * self.building_vol * (self.ach_inf / 3600)
                                      
                else: 
                     raise ValueError('Something went wrong with ventilation heat loss coefficient h_ve_adj')   
            
        return self.h_ve_adj
    
    
    def check_night_flushing(self, hour, t_out):
        """
        Checks if night flushing is on/off
        
        :param hour: Hour of the timestep
        :type hour: int
        :param t_out: Outdoor temperature of this timestep
        :type t_out: float

        :return: self.night_flushing_on
        :rtype: bool
        """
        
        
        daytime = hour%24                                   # Hour of the day
        cooling_season = (2169 < hour < 6561)               # Assume cooling season from 01/04 9am - 01/10 9am
        is_night_time = (daytime < 6 or daytime > 23)       # Define night time between 23:00 and 6:00
        
        # Use night flushing only if all conditions are satisfied: 
        # Night flushing needs to be available in the specific building, during cooling season,
        # during night time, indoor air temperature is higher than 21 °C and indoor air temp 
        # is higher than outdoor temp + 2 °C
        if self.night_flushing_flow > 0 \
            and (cooling_season == True) \
            and (is_night_time == True) \
            and (self.t_air > 21) \
            and (self.t_air > (t_out + 2)):
        
                self.night_flushing_on = True
        
        else:
                self.night_flushing_on = False
        
        return self.night_flushing_on
    
    
    def solve_building_lighting(self, illuminance, occupancy):
        """
        Calculates the lighting demand for a set timestep
        
        Daylighting is based on methods in 
        Szokolay, S.V. (1980): Environmental Science Handbook vor architects and builders. Unknown Edition, The Construction Press, Lancaster/London/New York, ISBN: 0-86095-813-2, p. 105ff.
        respectively
        Szokolay, S.V. (2008): Introduction to Architectural Science. The Basis of Sustainable Design. 2nd Edition, Elsevier/Architectural Press, Oxford, ISBN: 978-0-7506-8704-1, p. 154ff.


        :param illuminance: Illuminance transmitted through the window [Lumens]
        :type illuminance: float
        :param occupancy: Probability of full occupancy
        :type occupancy: float

        :return: self.lighting_demand, Lighting Energy Required for the timestep
        :rtype: float

        """
        lux = (illuminance * self.lighting_utilisation_factor *
               self.lighting_maintenance_factor) / self.net_room_area  # [Lux]

        if lux < self.lighting_control and occupancy > 0:
            # Lighting demand for the hour
            self.lighting_demand = self.lighting_load * self.net_room_area * occupancy
        else:
            self.lighting_demand = 0
              
            
    def solve_building_energy(self, internal_gains, solar_gains, t_out, t_m_prev):
        """
        Calculates the heating and cooling consumption of a building for a set timestep

        :param internal_gains: internal heat gains from people and appliances [W]
        :type internal_gains: float
        :param solar_gains: solar heat gains [W]
        :type solar_gains: float
        :param t_out: Outdoor air temperature [C]
        :type t_out: float
        :param t_m_prev: Previous air temperature [C]
        :type t_m_prev: float

        :return: self.heating_demand, space heating demand of the building
        :return: self.heating_sys_electricity, heating electricity consumption
        :return: self.heating_sys_fossils, heating fossil fuel consumption 
        :return: self.cooling_demand, space cooling demand of the building
        :return: self.cooling_sys_electricity, electricity consumption from cooling
        :return: self.cooling_sys_fossils, fossil fuel consumption from cooling
        :return: self.electricity_out, electricity produced from combined heat pump systems
        :return: self.sys_total_energy, total exergy consumed (electricity + fossils) for heating and cooling
        :return: self.heating_energy, total exergy consumed (electricity + fossils) for heating 
        :return: self.cooling_energy, total exergy consumed (electricity + fossils) for cooling
        :return: self.cop, Coefficient of Performance of the heating or cooling system
        :rtype: float

        """
        # Main File

        # check demand, and change state of self.has_heating_demand, and self._has_cooling_demand
        self.has_demand(internal_gains, solar_gains, t_out, t_m_prev)

        if not self.has_heating_demand and not self.has_cooling_demand:

            # no heating or cooling demand
            
            # calculate temperatures of building R-C-model and exit
            # --> rc_model_function_1(...)
            self.energy_demand = 0

            
            self.heating_demand = 0  # Energy required by the zone
            self.cooling_demand = 0  # Energy surplus of the zone
            # Energy (in electricity) required by the supply system to provide
            # HeatingDemand
            self.heating_sys_electricity = 0
            # Energy (in fossil fuel) required by the supply system to provide
            # HeatingDemand
            self.heating_sys_fossils = 0
            # Energy (in electricity) required by the supply system to get rid
            # of CoolingDemand
            self.cooling_sys_electricity = 0
            # Energy (in fossil fuel) required by the supply system to get rid
            # of CoolingDemand
            self.cooling_sys_fossils = 0
            # Electricity produced by the supply system (e.g. CHP)
            self.electricity_out = 0
            #Set COP to nan if no heating or cooling is required
            self.cop=float('nan')

        else:

            # has heating/cooling demand

            # Calculates energy_demand used below
            self.calc_energy_demand(
                internal_gains, solar_gains, t_out, t_m_prev)

            self.calc_temperatures_crank_nicolson(
                self.energy_demand, internal_gains, solar_gains, t_out, t_m_prev)
            # calculates the actual t_m resulting from the actual heating
            # demand (energy_demand)

            # Calculate the Heating/Cooling Input Energy Required

            supply_director = supply_system.SupplyDirector()  # Initialise Heating System Manager

            if self.has_heating_demand:
                supply_director.set_builder(self.heating_supply_system(load=self.energy_demand, 
                                                                t_out=t_out, 
                                                                heating_supply_temperature=self.heating_supply_temperature,
                                                                cooling_supply_temperature=self.cooling_supply_temperature, 
                                                                has_heating_demand=self.has_heating_demand, 
                                                                has_cooling_demand=self.has_cooling_demand))
                supplyOut = supply_director.calc_system()
                # All Variables explained underneath line 467
                self.heating_demand = self.energy_demand
                self.heating_sys_electricity = supplyOut.electricity_in
                self.heating_sys_fossils = supplyOut.fossils_in
                self.cooling_demand = 0
                self.cooling_sys_electricity = 0
                self.cooling_sys_fossils = 0
                self.electricity_out = supplyOut.electricity_out

            elif self.has_cooling_demand:
                supply_director.set_builder(self.cooling_supply_system(load=self.energy_demand * (-1), 
                                                                t_out=t_out, 
                                                                heating_supply_temperature=self.heating_supply_temperature,
                                                                cooling_supply_temperature=self.cooling_supply_temperature, 
                                                                has_heating_demand=self.has_heating_demand, 
                                                                has_cooling_demand=self.has_cooling_demand))
                supplyOut = supply_director.calc_system()
                self.heating_demand = 0
                self.heating_sys_electricity = 0
                self.heating_sys_fossils = 0
                self.cooling_demand = self.energy_demand
                self.cooling_sys_electricity = supplyOut.electricity_in
                self.cooling_sys_fossils = supplyOut.fossils_in
                self.electricity_out = supplyOut.electricity_out

            self.cop = supplyOut.cop

        self.sys_total_energy = self.heating_sys_electricity + self.heating_sys_fossils + \
            self.cooling_sys_electricity + self.cooling_sys_fossils
        self.heating_energy = self.heating_sys_electricity + self.heating_sys_fossils
        self.cooling_energy = self.cooling_sys_electricity + self.cooling_sys_fossils

    # TODO: rename. this is expected to return a boolean. instead, it changes state??? you don't want to change state...
    # why not just return has_heating_demand and has_cooling_demand?? then call the function "check_demand"
    # has_heating_demand, has_cooling_demand = self.check_demand(...)
    def has_demand(self, internal_gains, solar_gains, t_out, t_m_prev):
        """
        Determines whether the building requires heating or cooling
        Used in: solve_building_energy()

        # step 1 in section C.4.2 in [C.3 ISO 13790]
        """

        # set energy demand to 0 and see if temperatures are within the comfort
        # range
        energy_demand = 0
        # Solve for the internal temperature t_Air
        self.calc_temperatures_crank_nicolson(
            energy_demand, internal_gains, solar_gains, t_out, t_m_prev)

        # If the air temperature is less or greater than the set temperature,
        # there is a heating/cooling load
        if self.t_air < self.t_set_heating:
            self.has_heating_demand = True
            self.has_cooling_demand = False
        elif self.t_air > self.t_set_cooling:
            self.has_cooling_demand = True
            self.has_heating_demand = False
        else:
            self.has_heating_demand = False
            self.has_cooling_demand = False

    def calc_temperatures_crank_nicolson(self, energy_demand, internal_gains, solar_gains, t_out, t_m_prev):
        """
        Determines node temperatures (t_air, t_m, t_s) and computes derivation to determine the new node temperatures
        Used in: has_demand(), solve_building_energy(), calc_energy_demand()
        # section C.3 in [C.3 ISO 13790]
        """
        # Eq. C.1 - C.3
        self.calc_heat_flow(t_out, internal_gains, solar_gains, energy_demand)
        # Eq. C.5
        self.calc_phi_m_tot(t_out)

        # Calculates the new bulk temperature point from the old one
        # Eq. C.4
        self.calc_t_m_next(t_m_prev)

        # Calculates the average bulk temperature used for the remaining calculation
        # Eq. C.9
        self.calc_t_m(t_m_prev)
        # Eq. C.10
        self.calc_t_s(t_out)
        # Eq. C.11
        self.calc_t_air(t_out)

        return self.t_m, self.t_air, self.t_opperative

    def calc_energy_demand(self, internal_gains, solar_gains, t_out, t_m_prev):
        """
        Calculates the energy demand of the space if heating/cooling is active
        Used in: solve_building_energy()
        # Step 1 - Step 4 in Section C.4.2 in [C.3 ISO 13790]
        """

        # Step 1: Check if heating or cooling is needed 
        # (Not needed, but doing so for readability when comparing with the standard)
        # Set heating/cooling to 0
        energy_demand_0 = 0
        # Calculate the air temperature with no heating/cooling
        t_air_0 = self.calc_temperatures_crank_nicolson(
            energy_demand_0, internal_gains, solar_gains, t_out, t_m_prev)[1]

        # Step 2: Calculate the unrestricted heating/cooling required

        # determine if we need heating or cooling based based on the condition
        # that no heating or cooling is required
        if self.has_heating_demand:
            t_air_set = self.t_set_heating
        elif self.has_cooling_demand:
            t_air_set = self.t_set_cooling
        else:
            raise NameError(
                'heating function has been called even though no heating is required')

        # Set a heating case where the heating load is 10x the energy_ref_area (10
        # W/m2)
        energy_floorAx10 = 10 * self.energy_ref_area

        # Calculate the air temperature obtained by having this 10 W/m2
        # setpoint
        t_air_10 = self.calc_temperatures_crank_nicolson(
            energy_floorAx10, internal_gains, solar_gains, t_out, t_m_prev)[1]

        # Determine the unrestricted heating/cooling of the building
        self.calc_energy_demand_unrestricted(
            energy_floorAx10, t_air_set, t_air_0, t_air_10)

        # Step 3: Check if available heating or cooling power is sufficient
        # If max_cooling_energy_per_floor_area is set so -inf and 
        # max_heating_energy_per_floor_area to inf, this condition is always true
        if self.max_cooling_energy <= self.energy_demand_unrestricted <= self.max_heating_energy:

            self.energy_demand = self.energy_demand_unrestricted
            self.t_air_ac = t_air_set  # not sure what this is used for at this stage TODO

        # Step 4: if not sufficient then set the heating/cooling setting to the
        # maximum
        # necessary heating power exceeds maximum available power
        elif self.energy_demand_unrestricted > self.max_heating_energy:

            self.energy_demand = self.max_heating_energy

        # necessary cooling power exceeds maximum available power
        elif self.energy_demand_unrestricted < self.max_cooling_energy:

            self.energy_demand = self.max_cooling_energy

        else:
            self.energy_demand = 0
            raise ValueError('unknown radiative heating/cooling system status')

        # calculate system temperatures for Step 3/Step 4
        self.calc_temperatures_crank_nicolson(
            self.energy_demand, internal_gains, solar_gains, t_out, t_m_prev)

    def calc_energy_demand_unrestricted(self, energy_floorAx10, t_air_set, t_air_0, t_air_10):
        """
        Calculates the energy demand of the system if it has no maximum output restrictions
        # (C.13) in [C.3 ISO 13790]


        Based on the Thales Intercept Theorem. 
        Where we set a heating case that is 10x the floor area and determine the temperature as a result 
        Assuming that the relation is linear, one can draw a right angle triangle. 
        From this we can determine the heating level required to achieve the set point temperature
        This assumes a perfect HVAC control system
        """
        self.energy_demand_unrestricted = energy_floorAx10 * \
            (t_air_set - t_air_0) / (t_air_10 - t_air_0)

    def calc_heat_flow(self, t_out, internal_gains, solar_gains, energy_demand):
        """
        Calculates the heat flow from the solar gains, heating/cooling system, and internal gains into the building

        The input of the building is split into the air node, surface node, and thermal mass node based on
        on the following equations

        #C.1 - C.3 in [C.3 ISO 13790]

        Note that this equation has diverged slightly from the standard 
        as the heating/cooling node can enter any node depending on the
        emission system selected
        """

        # Calculates the heat flows to various points of the building based on the breakdown in section C.2, formulas C.1-C.3
        # Heat flow to the air node
        self.phi_ia = 0.5 * internal_gains
        # Heat flow to the surface node
        self.phi_st = (1 - (self.mass_area / self.A_t) - (self.h_tr_w /
                            (9.1 * self.A_t))) * (0.5 * internal_gains + solar_gains)
        # Heatflow to the thermal mass node
        self.phi_m = (self.mass_area / self.A_t) * \
            (0.5 * internal_gains + solar_gains)
        
        # We call the EmissionDirector to modify these flows depending on the
        # system and the energy demand
        emDirector = emission_system.EmissionDirector()

        # Set the emission system to the type specified by the user
        if energy_demand > 0:
            emDirector.set_builder(self.heating_emission_system(
                energy_demand=energy_demand))
        else:
            emDirector.set_builder(self.cooling_emission_system(
                energy_demand=energy_demand))
        # Calculate the new flows to each node based on the heating/cooling system
        flows = emDirector.calc_flows()

        # Set modified flows to building object
        self.phi_ia += flows.phi_ia_plus
        self.phi_st += flows.phi_st_plus
        self.phi_m += flows.phi_m_plus

        # Set supply temperature to building object
        self.heating_supply_temperature = flows.heating_supply_temperature
        self.cooling_supply_temperature = flows.cooling_supply_temperature
        
    def calc_t_m_next(self, t_m_prev):
        """
        Primary Equation, calculates the temperature of the next time step
        # (C.4) in [C.3 ISO 13790]
        """

        self.t_m_next = ((t_m_prev * ((self.c_m / 3600.0) - 0.5 * (self.h_tr_3 + self.h_tr_em))) +
                         self.phi_m_tot) / ((self.c_m / 3600.0) + 0.5 * (self.h_tr_3 + self.h_tr_em))

    def calc_phi_m_tot(self, t_out):
        """
        Calculates a global heat transfer. This is a definition used to simplify equation
        calc_t_m_next so it's not so long to write out
        # (C.5) in [C.3 ISO 13790]
        # h_ve = h_ve_adj and t_supply = t_out [9.3.2 ISO 13790]
        """

        t_supply = t_out  # ASSUMPTION: Supply air comes straight from the outside air

        self.phi_m_tot = self.phi_m + self.h_tr_em * t_out + \
            self.h_tr_3 * (self.phi_st + self.h_tr_w * t_out + self.h_tr_1 *
                           ((self.phi_ia / self.h_ve_adj) + t_supply)) / self.h_tr_2

    def calc_t_m(self, t_m_prev):
        """
        Temperature used for the calculations, average between newly calculated and previous bulk temperature
        # (C.9) in [C.3 ISO 13790]
        """
        self.t_m = (self.t_m_next + t_m_prev) / 2.0

    def calc_t_s(self, t_out):
        """
        Calculate the temperature of the inside room surfaces. 
        Consists of the air temperature and the average radiation temperature
        # (C.10) in [C.3 ISO 13790]
        # h_ve = h_ve_adj and t_supply = t_out [9.3.2 ISO 13790]
        """

        t_supply = t_out  # ASSUMPTION: Supply air comes straight from the outside air

        self.t_s = (self.h_tr_ms * self.t_m + self.phi_st + self.h_tr_w * t_out + self.h_tr_1 * \
            (t_supply + self.phi_ia / self.h_ve_adj)) / \
            (self.h_tr_ms + self.h_tr_w + self.h_tr_1)

    def calc_t_air(self, t_out):
        """
        Calculate the temperature of the air node
        # (C.11) in [C.3 ISO 13790]
        # h_ve = h_ve_adj and t_supply = t_out [9.3.2 ISO 13790]
        """

        t_supply = t_out

        # Calculate the temperature of the inside air
        self.t_air = (self.h_tr_is * self.t_s + self.h_ve_adj *
                      t_supply + self.phi_ia) / (self.h_tr_is + self.h_ve_adj)
        
       
        
      