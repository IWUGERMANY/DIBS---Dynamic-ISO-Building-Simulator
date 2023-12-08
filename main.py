import sys
import os
paths = [os.path.abspath(os.path.join(os.path.dirname(__file__), ''))]
sys.path[:0] = paths

from iso_simulator.model.epw_file import EPWFile
from iso_simulator.model.building import Building
from iso_simulator.building_simulator.simulator import BuildingSimulator
from iso_simulator.model.location import Location

from iso_simulator.data_source.datasource_csv import DataSourceCSV






def main():
    # building_simulator: BuildingSimulator = BuildingSimulator(
    #     DataSourceCSV(), "2004-2018", 'din', 'low')
    # building_data: Building = building_simulator.datasourcecsv.get_building_data()
    # gwp_pe_factors = building_simulator.datasourcecsv.get_epw_pe_factors()
    # building_simulator.initialize_building_time()
    # building_simulator.check_energy_area_and_heating()
    # epw_file_object: EPWFile = building_simulator.datasourcecsv.get_epw_file(
    #     building_data.plz, building_simulator.weather_period)
    # weather_data = building_simulator.get_weather_data()
    #
    # windows = building_simulator.build_windows_objects()
    #
    # gain_person_and_typ_norm, appliance_gains = building_simulator.datasourcecsv.get_gains(
    #     building_data.hk_geb, building_data.uk_geb, building_simulator.profile_from_norm,
    #     building_simulator.gains_from_group_values)
    #
    # usage_start, usage_end = building_simulator.get_usage_start_and_end()
    # occupancy_schedule, schedule_name = building_simulator.get_schedule()
    #
    # tek_dhw, tek_name = building_simulator.get_tek()
    #
    # occupancy_full_usage_hours = building_simulator.get_occupancy_full_usage_hours()
    #
    # tek_dhw_per_occupancy_full_usage_hour = tek_dhw / occupancy_full_usage_hours
    #
    # t_m_prev = building_data.t_start

    for hour in range(1):
        t_out = building_simulator.extract_outdoor_temperature(
            weather_data, hour)

        altitude, azimuth = Location.calc_sun_position(Location(
        ), epw_file_object.coordinates_station[0], epw_file_object.coordinates_station[1], weather_data[hour].year,
            hour)

        building_data.h_ve_adj = building_data.calc_h_ve_adj(
            hour, t_out, usage_start, usage_end)

        t_air = building_data.t_set_heating if hour == 0 else building_data.t_air


        # building_simulator.calc_solar_gains_for_all_windows(
        #     weather_data, 3.9679769725374214, 44.92407457491144, 21.0, 8)
        # print(f'hour 8, solar gains: {building_simulator.all_windows[0].solar_gains}, incident solar: {building_simulator.all_windows[0].incident_solar}')

        # building_simulator.calc_solar_gains_for_all_windows(
        #     weather_data, 1.6129081206543545, -49.008898042516094, 20.999999999999982, 15)
        # print(f'hour 15, solar gains: {building_simulator.all_windows[0].solar_gains}, incident solar: {building_simulator.all_windows[0].incident_solar}')
        # building_simulator.all_windows[0]
        # building_simulator.calc_illuminance_for_all_windows(
        #     weather_data, altitude, azimuth, t_air, hour)

        # building_simulator.calc_solar_gains_for_all_windows(
        #     weather_data, 3.9679769725374214, 44.92407457491144, 21.0, 8)
        # south_window = building_simulator.all_windows[0].incident_solar
        # print(building_simulator.all_windows[0].solar_gains, building_simulator.all_windows[0].incident_solar )

        building_simulator.calc_solar_gains_for_all_windows(
            weather_data, 3.9679769725374214, 44.92407457491144, 21.0, 8)
        south_window = building_simulator.all_windows[0].incident_solar


if __name__ == '__main__':
    main()

print(dir(locals()['__builtins__']))