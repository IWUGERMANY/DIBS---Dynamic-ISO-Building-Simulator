"""
Supply System Parameters for Heating and Cooling

Model of different Supply systems. New Supply Systems can be introduced by adding new classes

TODO: Have a look at CEA calculation methodology 
https://github.com/architecture-building-systems/CEAforArcGIS/blob/master/cea/technologies/heatpumps.py


Portions of this software are copyright of their respective authors and released under the MIT license:
RC_BuildingSimulator, Copyright 2016 Architecture and Building Systems, ETH Zurich

author: "Simon Knoll, Julian Bischof, Michael Hörner "
copyright: "Copyright 2021, Institut Wohnen und Umwelt"
license: "MIT"

"""
__author__ = "Simon Knoll, Julian Bischof, Michael Hörner "
__copyright__ = "Copyright 2022, Institut Wohnen und Umwelt"
__license__ = "MIT"



class SupplyDirector:

    """
    The director sets what Supply system is being used, and runs that set Supply system
    """

    builder = None

    # Sets what building system is used
    def set_builder(self, builder):
        self.builder = builder

    # Calcs the energy load of that system. This is the main() function
    def calc_system(self):

        # Director asks the builder to produce the system body. self.builder
        # is an instance of the class

        body = self.builder.calc_loads()

        return body


class SupplySystemBase:

    """
     The base class in which Supply systems are built from 
    """

    def __init__(self, load, t_out, heating_supply_temperature, cooling_supply_temperature, has_heating_demand, has_cooling_demand):
        self.load = load  # Energy Demand of the building at that time step
        self.t_out = t_out  # Outdoor Air Temperature
        # Temperature required by the emission system
        self.heating_supply_temperature = heating_supply_temperature
        self.cooling_supply_temperature = cooling_supply_temperature
        self.has_heating_demand = has_heating_demand
        self.has_cooling_demand = has_cooling_demand

    def calc_loads(self): pass
    """
    Caculates the electricty / fossil fuel consumption of the set supply system
    If the system also generates electricity, then this is stored as electricity_out
    """
    
    
##############################################################################
# Oil Boilers 
##############################################################################    
class OilBoilerStandardBefore86(SupplySystemBase):
    """
    expenditure factor (=Erzeugeraufwandszahl) from TEK-Tool 9.24
    Konstanttemperaturkessel 78-86 - Oil
    """

    def calc_loads(self):
        system = SupplyOut()
        system.fossils_in = self.load * 1.114
        system.electricity_in = 0
        system.electricity_out = 0
        return system

class OilBoilerStandardFrom95(SupplySystemBase):
    """
    expenditure factor (=Erzeugeraufwandszahl) from TEK-Tool 9.24
    Konstanttemperaturkessel ab 1995 - Oil
    """

    def calc_loads(self):
        system = SupplyOut()
        system.fossils_in = self.load * 1.087
        system.electricity_in = 0
        system.electricity_out = 0
        return system

class OilBoilerLowTempBefore87(SupplySystemBase):
    """
    expenditure factor (=Erzeugeraufwandszahl) from TEK-Tool 9.24
    Niedertemperaturkessel vor 1987 - Oil
    """

    def calc_loads(self):
        system = SupplyOut()
        system.fossils_in = self.load * 1.112
        system.electricity_in = 0
        system.electricity_out = 0
        return system    

class OilBoilerLowTempBefore95(SupplySystemBase):
    """
    expenditure factor (=Erzeugeraufwandszahl) from TEK-Tool 9.24
    Niedertemperaturkessel vor 1995 - Oil
    """

    def calc_loads(self):
        system = SupplyOut()
        system.fossils_in = self.load * 1.086
        system.electricity_in = 0
        system.electricity_out = 0
        return system
    
class OilBoilerLowTempFrom95(SupplySystemBase):
    """
    expenditure factor (=Erzeugeraufwandszahl) from TEK-Tool 9.24
    Niedertemperaturkessel ab 1995 - Oil
    """

    def calc_loads(self):
        system = SupplyOut()
        system.fossils_in = self.load * 1.067
        system.electricity_in = 0
        system.electricity_out = 0
        return system
    
class OilBoilerCondensingBefore95(SupplySystemBase):
    """
    expenditure factor (=Erzeugeraufwandszahl) from TEK-Tool 9.24
    Brennwertkessel vor 1995 - Oil 
    """

    def calc_loads(self):
        system = SupplyOut()
        system.fossils_in = self.load * 1.03
        system.electricity_in = 0
        system.electricity_out = 0
        return system
    
class OilBoilerCondensingFrom95(SupplySystemBase):
    """
    expenditure factor (=Erzeugeraufwandszahl) from TEK-Tool 9.24
    Brennwertkessel ab 1995 - Oil 
    """

    def calc_loads(self):
        system = SupplyOut()
        system.fossils_in = self.load * 1.028
        system.electricity_in = 0
        system.electricity_out = 0
        return system

class OilBoilerCondensingImproved(SupplySystemBase):
    """
    expenditure factor (=Erzeugeraufwandszahl) from TEK-Tool 9.24
    Brennwertkessel verbessert 
    """

    def calc_loads(self):
        system = SupplyOut()
        system.fossils_in = self.load * 1.004
        system.electricity_in = 0
        system.electricity_out = 0
        return system


##############################################################################
# Gas Boilers
##############################################################################    
class GasBoilerStandardBefore86(SupplySystemBase):
    """
    expenditure factor (=Erzeugeraufwandszahl) from TEK-Tool 9.24
    Konstanttemperaturkessel vor 1986 - Gas
    """

    def calc_loads(self):
        system = SupplyOut()
        system.fossils_in = self.load * 1.142
        system.electricity_in = 0
        system.electricity_out = 0
        return system
    
class GasBoilerStandardBefore95(SupplySystemBase):
    """
    expenditure factor (=Erzeugeraufwandszahl) from TEK-Tool 9.24
    Konstanttemperaturkessel vor 1995 (87-94) - Gas
    """

    def calc_loads(self):
        system = SupplyOut()
        system.fossils_in = self.load * 1.124
        system.electricity_in = 0
        system.electricity_out = 0
        return system 
    
class GasBoilerStandardFrom95(SupplySystemBase):
    """
    expenditure factor (=Erzeugeraufwandszahl) from TEK-Tool 9.24
    Konstanttemperaturkessel ab 1995 - Gas
    """

    def calc_loads(self):
        system = SupplyOut()
        system.fossils_in = self.load * 1.114
        system.electricity_in = 0
        system.electricity_out = 0
        return system    

class GasBoilerLowTempBefore87(SupplySystemBase):
    """
    expenditure factor (=Erzeugeraufwandszahl) from TEK-Tool 9.24
    Niedertemperaturkessel vor 1987 - Gas
    """

    def calc_loads(self):
        system = SupplyOut()
        system.fossils_in = self.load * 1.14
        system.electricity_in = 0
        system.electricity_out = 0
        return system
    
class LGasBoilerLowTempBefore87(SupplySystemBase):
    """
    expenditure factor (=Erzeugeraufwandszahl) from TEK-Tool 9.24
    Niedertemperaturkessel vor 1987 - L-Gas
    """

    def calc_loads(self):
        system = SupplyOut()
        system.fossils_in = self.load * 1.129
        system.electricity_in = 0
        system.electricity_out = 0
        return system
    
class GasBoilerLowTempBefore95(SupplySystemBase):
    """
    expenditure factor (=Erzeugeraufwandszahl) from TEK-Tool 9.24
    Niedertemperaturkessel vor 1995 - Gas
    """

    def calc_loads(self):
        system = SupplyOut()
        system.fossils_in = self.load * 1.113
        system.electricity_in = 0
        system.electricity_out = 0
        return system
    
class LGasBoilerLowTempBefore95(SupplySystemBase):
    """
    expenditure factor (=Erzeugeraufwandszahl) from TEK-Tool 9.24
    Niedertemperaturkessel vor 1995 - L-Gas
    """

    def calc_loads(self):
        system = SupplyOut()
        system.fossils_in = self.load * 1.102
        system.electricity_in = 0
        system.electricity_out = 0
        return system 

class GasBoilerLowTempFrom95(SupplySystemBase):
    """
    expenditure factor (=Erzeugeraufwandszahl) from TEK-Tool 9.24
    Niedertemperaturkessel ab 1995 - Gas
    """

    def calc_loads(self):
        system = SupplyOut()
        system.fossils_in = self.load * 1.095
        system.electricity_in = 0
        system.electricity_out = 0
        return system
    
class LGasBoilerLowTempFrom95(SupplySystemBase):
    """
    expenditure factor (=Erzeugeraufwandszahl) from TEK-Tool 9.24
    Niedertemperaturkessel ab 1995 - L-Gas
    """

    def calc_loads(self):
        system = SupplyOut()
        system.fossils_in = self.load * 1.083
        system.electricity_in = 0
        system.electricity_out = 0
        return system  

class BiogasOilBoilerLowTempBefore95(SupplySystemBase):
    """
    expenditure factor (=Erzeugeraufwandszahl) from TEK-Tool 9.24
    Niedertemperaturkessel vor 1995 - Biogas/Bioöl Mix
    """

    def calc_loads(self):
        system = SupplyOut()
        system.fossils_in = self.load * 1.0995
        system.electricity_in = 0
        system.electricity_out = 0
        return system  
    
    
class GasBoilerLowTempSpecialFrom78(SupplySystemBase):
    """
    expenditure factor (=Erzeugeraufwandszahl) from TEK-Tool 9.24
    Niedertemperaturkessel-Spezialkessel ab 1978 - Gas
    """

    def calc_loads(self):
        system = SupplyOut()
        system.fossils_in = self.load * 1.113
        system.electricity_in = 0
        system.electricity_out = 0
        return system   
    
class GasBoilerLowTempSpecialFrom95(SupplySystemBase):
    """
    expenditure factor (=Erzeugeraufwandszahl) from TEK-Tool 9.24
    Niedertemperaturkessel-Spezialkessel ab 1995 - Gas
    """

    def calc_loads(self):
        system = SupplyOut()
        system.fossils_in = self.load * 1.093
        system.electricity_in = 0
        system.electricity_out = 0
        return system         

class GasBoilerCondensingBefore95(SupplySystemBase):
    """
    expenditure factor (=Erzeugeraufwandszahl) from TEK-Tool 9.24
    Brennwertkessel vor 1995 - Gas
    """

    def calc_loads(self):
        system = SupplyOut()
        system.fossils_in = self.load * 1.057
        system.electricity_in = 0
        system.electricity_out = 0
        return system    
    
class LGasBoilerCondensingBefore95(SupplySystemBase):
    """
    expenditure factor (=Erzeugeraufwandszahl) from TEK-Tool 9.24
    Brennwertkessel vor 1995 - L-Gas
    """

    def calc_loads(self):
        system = SupplyOut()
        system.fossils_in = self.load * 1.047
        system.electricity_in = 0
        system.electricity_out = 0
        return system       
    
class BiogasBoilerCondensingBefore95(SupplySystemBase):
    """
    expenditure factor (=Erzeugeraufwandszahl) from TEK-Tool 9.24
    Brennwertkessel vor 1995 - Biogas
    """

    def calc_loads(self):
        system = SupplyOut()
        system.fossils_in = self.load * 1.057
        system.electricity_in = 0
        system.electricity_out = 0
        return system  

class BiogasBoilerCondensingFrom95(SupplySystemBase):
    """
    expenditure factor (=Erzeugeraufwandszahl) from TEK-Tool 9.24
    Brennwertkessel nach 1995 - Biogas
    """

    def calc_loads(self):
        system = SupplyOut()
        system.fossils_in = self.load * 1.054
        system.electricity_in = 0
        system.electricity_out = 0
        return system 
        
    
class GasBoilerCondensingFrom95(SupplySystemBase):
    """
    expenditure factor (=Erzeugeraufwandszahl) from TEK-Tool 9.24
    Brennwertkessel ab 1995 - Gas
    """

    def calc_loads(self):
        system = SupplyOut()
        system.fossils_in = self.load * 1.054
        system.electricity_in = 0
        system.electricity_out = 0
        return system    
    
class LGasBoilerCondensingFrom95(SupplySystemBase):
    """
    expenditure factor (=Erzeugeraufwandszahl) from TEK-Tool 9.24
    Brennwertkessel ab 1995 - L-Gas
    """

    def calc_loads(self):
        system = SupplyOut()
        system.fossils_in = self.load * 1.044
        system.electricity_in = 0
        system.electricity_out = 0
        return system     

# Double of above BiogasBoilerCondensingFrom95    
# class BioGasBoilerCondensingFrom95(SupplySystemBase):
#     """
#     expenditure factor (=Erzeugeraufwandszahl) from TEK-Tool 9.24
#     Brennwertkessel ab 1995 - Biogas
#     """

#     def calc_loads(self):
#         system = SupplyOut()
#         system.fossils_in = self.load * 1.054
#         system.electricity_in = 0
#         system.electricity_out = 0
#         return system      
    
class BiogasOilBoilerCondensingFrom95(SupplySystemBase):
    """
    expenditure factor (=Erzeugeraufwandszahl) from TEK-Tool 9.24
    Brennwertkessel ab 1995 - Biogas/Bioöl Mix 
    """

    def calc_loads(self):
        system = SupplyOut()
        system.fossils_in = self.load * 1.041
        system.electricity_in = 0
        system.electricity_out = 0
        return system 
    
class GasBoilerCondensingImproved(SupplySystemBase):
    """
    expenditure factor (=Erzeugeraufwandszahl) from TEK-Tool 9.24
    Brennwertkessel verbessert - Gas
    """

    def calc_loads(self):
        system = SupplyOut()
        system.fossils_in = self.load * 1.028
        system.electricity_in = 0
        system.electricity_out = 0
        return system    

class LGasBoilerCondensingImproved(SupplySystemBase):
    """
    expenditure factor (=Erzeugeraufwandszahl) from TEK-Tool 9.24
    Brennwertkessel verbessert - L-Gas
    """

    def calc_loads(self):
        system = SupplyOut()
        system.fossils_in = self.load * 1.019
        system.electricity_in = 0
        system.electricity_out = 0
        return system   
    
class BiogasOilBoilerCondensingImproved(SupplySystemBase):
    """
    expenditure factor (=Erzeugeraufwandszahl) from TEK-Tool 9.24
    Brennwertkessel verbessert - Biogas/Bioöl Mix
    """

    def calc_loads(self):
        system = SupplyOut()
        system.fossils_in = self.load * 1.016
        system.electricity_in = 0
        system.electricity_out = 0
        return system       
    
    
##############################################################################
# Solid Fuel Boilers 
##############################################################################
class WoodChipSolidFuelBoiler(SupplySystemBase):
    """
    expenditure factor (=Erzeugeraufwandszahl) from TEK-Tool 9.24
    Feststoffkessel mit Pufferspeicher ab 95 (Holzhack)
    """

    def calc_loads(self):
        system = SupplyOut()
        system.fossils_in = self.load * 1.056
        system.electricity_in = 0
        system.electricity_out = 0
        return system        

class WoodPelletSolidFuelBoiler(SupplySystemBase):
    """
    expenditure factor (=Erzeugeraufwandszahl) from TEK-Tool 9.24
    Feststoffkessel mit Pufferspeicher ab 95 (Holzpellet)
    """

    def calc_loads(self):
        system = SupplyOut()
        system.fossils_in = self.load * 1.054
        system.electricity_in = 0
        system.electricity_out = 0
        return system  

class WoodSolidFuelBoilerCentral(SupplySystemBase):
    """
    expenditure factor (=Erzeugeraufwandszahl) from TEK-Tool 9.24
    Feststoffkessel ab (ohne Puffer) 95 (Holzhack/Pellets Mix)
    """

    def calc_loads(self):
        system = SupplyOut()
        system.fossils_in = self.load * 1.123
        system.electricity_in = 0
        system.electricity_out = 0
        return system    

class CoalSolidFuelBoiler(SupplySystemBase):
    """
    expenditure factor (=Erzeugeraufwandszahl) from TEK-Tool 9.24
    Mix between Feststoffkessel 78-94 (Kohle) - Steinkohle
    and Feststoffkessel 78-94 (Kohle) - Braunkohle
    """

    def calc_loads(self):
        system = SupplyOut()
        system.fossils_in = self.load * 1.123
        system.electricity_in = 0
        system.electricity_out = 0
        return system      
    
##############################################################################
# Furnaces
##############################################################################    
class SolidFuelLiquidFuelFurnace(SupplySystemBase):
    """
    Minimum efficiency according to '1. BImSchV, Anlage 4'
    """

    def calc_loads(self):
        system = SupplyOut()
        system.fossils_in = self.load / 0.7
        system.electricity_in = 0
        system.electricity_out = 0
        return system   
  
##############################################################################
# Heat Pumps
##############################################################################
class HeatPumpAirSource(SupplySystemBase):
    """
    BETA Version
    COP based off regression analysis of manufacturers data
    Source: Staffell et al. (2012): A review of domestic heat pumps, In: Energy & Environmental Science, 2012, 5, p. 9291-9306
    """

    def calc_loads(self):
        system = SupplyOut()

        if self.has_heating_demand:
            # determine the temperature difference, if negative, set to 0
            deltaT = max(0, self.heating_supply_temperature - self.t_out)
            # Eq (4) in Staggell et al.
            system.cop = 6.81 - 0.121 * deltaT + 0.000630 * deltaT**2
            system.electricity_in = self.load / system.cop

        elif self.has_cooling_demand:
            # determine the temperature difference, if negative, set to 0
            deltaT = max(0, self.t_out - self.cooling_supply_temperature)
            # Eq (4) in Staggell et al.
            system.cop = 6.81 - 0.121 * deltaT + 0.000630 * deltaT**2
            system.electricity_in = self.load / system.cop

        else:
            raise ValueError(
                'HeatPumpAir called although there is no heating/cooling demand')

        system.fossils_in = 0
        system.electricity_out = 0
        return system

class HeatPumpGroundSource(SupplySystemBase):
    """"
    BETA Version
    Ground source heat pumps can be designed in an open-loop system where they "extract water directly from, and reject it
    back to rivers or groundwater resources such as aquifers and springs" or in an closed-loop system where they use "a 
    sealed loop to extract heat from the surrounding soil or rock". 
    Source: Staffell et al. (2012): A review of domestic heat pumps, In: Energy & Environmental Science, 2012, 5, p. 9291-9306

    Reservoir temperatures 7 degC (winter) and 12 degC (summer). 
    COP based on regression analysis of manufacturers data
    Source: Staffell et al. (2012): A review of domestic heat pumps, In: Energy & Environmental Science, 2012, 5, p. 9291-9306
    """


    def calc_loads(self):
        system = SupplyOut()
        if self.has_heating_demand:
            deltaT = max(0, self.heating_supply_temperature - 7.0)
            # Eq (4) in Staggell et al.
            system.cop = 8.77 - 0.150 * deltaT + 0.000734 * deltaT**2
            system.electricity_in = self.load / system.cop

        elif self.has_cooling_demand:
            deltaT = max(0, 13.0 - self.cooling_supply_temperature)
            # Eq (4) in Staggell et al.
            system.cop = 8.77 - 0.150 * deltaT + 0.000734 * deltaT**2
            system.electricity_in = self.load / system.cop

        system.fossils_in = 0
        system.electricity_out = 0
        return system
    
    
##############################################################################
# Combined heat and power plant
##############################################################################
class GasCHP(SupplySystemBase):
    """
    Combined heat and power unit with 49 percent thermal and 38 percent
    electrical efficiency. Source: Arbeitsgemeinschaft für sparsamen und umwelfreundlichen Energieverbrauch e.V. (2011): BHKW-Kenndasten 2011
    """

    def calc_loads(self):
        system = SupplyOut()
        system.fossils_in = self.load / 0.49
        system.electricity_in = 0
        system.electricity_out = system.fossils_in * 0.38
        return system
    
    
##############################################################################
# District Heating
# Assumption: Indirect system with two water circuits          
##############################################################################
class DistrictHeating(SupplySystemBase):
    """
    expenditure factor (=Erzeugeraufwandszahl) from TEK-Tool 9.24
    District Heating with expenditure factor = 1.002
    """
    
    def calc_loads(self):
        system = SupplyOut()
        system.fossils_in = self.load * 1.002
        system.electricity_in = 0
        system.electricity_out = 0
        return system       
  

##############################################################################
# Electric Heating   
##############################################################################
class ElectricHeating(SupplySystemBase):
    """
    Straight forward electric heating. 100 percent conversion to heat.
    """

    def calc_loads(self):
        system = SupplyOut()
        system.electricity_in = self.load
        system.fossils_in = 0
        system.electricity_out = 0
        return system
    
    
##############################################################################
# Direct Heater for testing purposes
##############################################################################  
class DirectHeater(SupplySystemBase):
    """
    Created by PJ to check accuracy against previous simulation
    """

    def calc_loads(self):
        system = SupplyOut()
        system.electricity_in = self.load
        system.fossils_in = 0
        system.electricity_out = 0
        return system
    
    
##############################################################################
# AirCooledPistonScroll
##############################################################################
class AirCooledPistonScroll(SupplySystemBase):
    """
    Wärmeabfuhr Kältemaschine (Kondensator): Luftgekühlt (Primärkreis)
    Verdichterart: Kolben-/Scrollverdichter - on/off Betrieb
    
    Informationsblatt zur Kälteerzeugung gemäss Norm SIA 382-1:2014, S. 4
    Kälteerzeugerleistung der Kältemaschine: 100 kW
    EER (full load): 3,1
    """

    def calc_loads(self):
        system = SupplyOut()
        system.electricity_in = self.load / 3.1
        system.fossils_in = 0
        system.electricity_out = 0
        return system    
    

##############################################################################
# AirCooledPistonScrollMulti
##############################################################################
class AirCooledPistonScrollMulti(SupplySystemBase):
    """
    Wärmeabfuhr Kältemaschine (Kondensator): Luftgekühlt (Primärkreis)
    Verdichterart: Kolben-/Scrollverdichter - mehrstufig
    
    Informationsblatt zur Kälteerzeugung gemäss Norm SIA 382-1:2014
    Kälteerzeugerleistung der Kältemaschine: 100 kW
    EER (full load): 3,1
    """

    def calc_loads(self):
        system = SupplyOut()
        system.electricity_in = self.load / 3.1
        system.fossils_in = 0
        system.electricity_out = 0
        return system 
    
  
##############################################################################
# WaterCooledPistonScroll
##############################################################################
class WaterCooledPistonScroll(SupplySystemBase):
    """
    Wärmeabfuhr Kältemaschine (Kondensator): Wassergekühlt (Primärkreis)
    Verdichterart: Kolben-/Scrollverdichter - on/off Betrieb
    
    Informationsblatt zur Kälteerzeugung gemäss Norm SIA 382-1:2014
    Kälteerzeugerleistung der Kältemaschine: 100 kW
    EER (full load): 4,25
    """

    def calc_loads(self):
        system = SupplyOut()
        system.electricity_in = self.load / 3.2
        system.fossils_in = 0
        system.electricity_out = 0
        return system

    
##############################################################################
# AbsorptionRefrigerationSystem
##############################################################################
class AbsorptionRefrigerationSystem(SupplySystemBase):
    """
    Wärmeabfuhr Kältemaschine (Kondensator): Wassergekühlt (Primärkreis)
    Verdichterart: Absorptionskälteanlage H2O/LiBr
      
    Assumption: Driving heat comes from waste heat, not from fossils (this may lead to biased results if this is not the case), due to the fact that
    absorption chillers usually have a lower efficiency compared to compression chillers. We assume that building owners only use absorption chillers if 
    they have access to heat free of charge.
    
    Furthermore: Electricity consumption for pumps etc. are not considered at this stage
    """

    def calc_loads(self):
        system = SupplyOut()
        system.electricity_in = 0
        system.fossils_in = 0
        system.electricity_out = 0
        return system
   
    
##############################################################################
# DistrictCooling
##############################################################################
class DistrictCooling(SupplySystemBase):
    """
    DistrictCooling assumed with efficiency 100%
    """

    def calc_loads(self):
        system = SupplyOut()
        system.electricity_in = 0
        system.fossils_in = self.load
        system.electricity_out = 0
        return system   
    

##############################################################################
# GasEnginePistonScroll #https://d-nb.info/1047203537/34 
##############################################################################
class GasEnginePistonScroll(SupplySystemBase):
    """
    ANALYSIS OF ENERGY EFFICIENCY OF GAS DRIVEN HEAT PUMPS - PhD Work of
    M.Sc. Essam Mahrous Elgenady Elgendy
    Fakultaet fuer Verfahrens- und Systemtechnik 
    der Otto-von-Guericke-Universitaet Magdeburg
    """

    def calc_loads(self):
        system = SupplyOut()
        system.electricity_in = 0
        system.fossils_in = self.load / 1.16 
        system.electricity_out = 0
        return system

##############################################################################
# Direct Cooler for testing purposes
##############################################################################
class DirectCooler(SupplySystemBase):
    """
    Created by PJ to check accuracy against previous simulation
    """

    def calc_loads(self):
        system = SupplyOut()
        system.electricity_in = self.load
        system.fossils_in = 0
        system.electricity_out = 0
        return system
    
##############################################################################
# NoHeating
##############################################################################
class NoHeating(SupplySystemBase):
    """
    Dummyclass used for buildings with no heating supply system
    """

    def calc_loads(self):
        system = SupplyOut()
        system.electricity_in = 0
        system.fossils_in = 0
        system.electricity_out = 0
        return system  

    
##############################################################################
# NoCooling
##############################################################################
class NoCooling(SupplySystemBase):
    """
    Dummyclass used for buildings with no cooling supply system
    """

    def calc_loads(self):
        system = SupplyOut()
        system.electricity_in = 0
        system.fossils_in = 0
        system.electricity_out = 0
        return system    
    
    
##############################################################################
##############################################################################

class SupplyOut:
    """
    The System class which is used to output the final results
    """
    fossils_in = float("nan")
    electricity_in = float("nan")
    electricity_out = float("nan")
    cop = float("nan")
