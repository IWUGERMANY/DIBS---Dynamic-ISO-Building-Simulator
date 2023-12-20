from iso_simulator.data_source.datasource_csv import DataSourceCSV
from iso_simulator.dibs.dibs import DIBS
from iso_simulator.building_simulator.simulator import BuildingSimulator


def main():
    datasource = DataSourceCSV()
    dibs = DIBS(datasource)
    simulator = BuildingSimulator(datasource, "2004-2018", 'din18599', 'mid', 'sia2024')

    # dibs.calc_one_building(simulator)
    dibs.calc_multiple_buildings(simulator)

if __name__ == '__main__':
    main()
