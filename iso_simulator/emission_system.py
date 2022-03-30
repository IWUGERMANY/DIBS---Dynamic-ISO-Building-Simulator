"""
Emission System Parameters for Heating and Cooling

Model of different Emission systems. New Emission Systems can be introduced by adding new classes

Temperatures only relevant in combination with heat pumps at this stage 
Temperatures taken from RC_BuildingSimulator and CEA (https://github.com/architecture-building-systems/CityEnergyAnalyst/blob/master/cea/databases/CH/assemblies/HVAC.xls)


Portions of this software are copyright of their respective authors and released under the MIT license:
RC_BuildingSimulator, Copyright 2016 Architecture and Building Systems, ETH Zurich

author: "Simon Knoll, Julian Bischof, Michael Hörner "
copyright: "Copyright 2021, Institut Wohnen und Umwelt"
license: "MIT"

"""
__author__ = "Simon Knoll, Julian Bischof, Michael Hörner "
__copyright__ = "Copyright 2022, Institut Wohnen und Umwelt"
__license__ = "MIT"


class EmissionDirector:

    """
    The director sets what Emission system is being used, and runs that set Emission system
    """

    builder = None

    # Sets what Emission system is used
    def set_builder(self, builder):
        # self.__builder = builder
        self.builder = builder
    # Calcs the energy load of that system. This is the main() fu

    def calc_flows(self):

        # Director asks the builder to produce the system body. self.builder
        # is an instance of the class

        body = self.builder.heat_flows()

        return body


class EmissionSystemBase:

    """ 
    The base class in which systems are built from
    """

    def __init__(self, energy_demand):

        self.energy_demand = energy_demand


    def heat_flows(self): pass
    """
    determines the node where the heating/cooling system is active based on the system used
    Also determines the return and supply temperatures for the heating/cooling system
    """
    

class AirConditioning(EmissionSystemBase):
    """
    All heat is given to the air via an AC-unit. HC input via the air node as in the ISO 13790 Annex C
    Temperatures taken from RC_BuildingSimulator [new radiators (assumption)]
    Heat is emitted to the air node
    """

    def heat_flows(self):
        flows = Flows()
        flows.phi_ia_plus = self.energy_demand
        flows.phi_st_plus = 0
        flows.phi_m_plus = 0

        flows.heating_supply_temperature = 40
        flows.heating_return_temperature = 20
        flows.cooling_supply_temperature = 12
        flows.cooling_return_temperature = 21

        return flows
    
    
class SurfaceHeatingCooling(EmissionSystemBase):
    """
    All HC energy goes into the surface node, assumed low supply temperature 
    Heat is emitted to the surface node
    """

    def heat_flows(self):
        flows = Flows()
        flows.phi_ia_plus = 0
        flows.phi_st_plus = self.energy_demand
        flows.phi_m_plus = 0

        flows.heating_supply_temperature = 40
        flows.heating_return_temperature = 35
        flows.cooling_supply_temperature = 12
        flows.cooling_return_temperature = 21

        return flows
    
    
class ThermallyActivated(EmissionSystemBase):
    """
    Heat is emitted to the thermal mass node, assumed low supply temperature 
    """

    def heat_flows(self):
        flows = Flows()
        flows.phi_ia_plus = 0
        flows.phi_st_plus = 0
        flows.phi_m_plus = self.energy_demand

        flows.heating_supply_temperature = 40
        flows.heating_return_temperature = 35
        flows.cooling_supply_temperature = 12
        flows.cooling_return_temperature = 21

        return flows


class NoCooling(EmissionSystemBase):
    """
    Dummy Class used for buildings with no cooling supply system
    """

    def heat_flows(self):
        flows = Flows()
        flows.phi_ia_plus = 0
        flows.phi_st_plus = 0
        flows.phi_m_plus = 0

        flows.heating_supply_temperature = 0
        flows.heating_return_temperature = 0
        flows.cooling_supply_temperature = 0
        flows.cooling_return_temperature = 0

        return flows 
    
    
class NoHeating(EmissionSystemBase):
    """
    Dummy Class used for buildings with no heating supply system
    """

    def heat_flows(self):
        flows = Flows()
        flows.phi_ia_plus = 0
        flows.phi_st_plus = 0
        flows.phi_m_plus = 0

        flows.heating_supply_temperature = 0
        flows.heating_return_temperature = 0
        flows.cooling_supply_temperature = 0
        flows.cooling_return_temperature = 0

        return flows       


class Flows:
    """
    A base object to store output variables
    """

    phi_ia_plus = float("nan")
    phi_m_plus = float("nan")
    phi_st_plus = float("nan")

    heating_supply_temperature = float("nan")
    cooling_supply_temperature = float("nan")
    # return temperatures
