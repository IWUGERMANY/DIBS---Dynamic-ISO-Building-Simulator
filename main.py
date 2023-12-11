import sys
import os

paths = [os.path.abspath(os.path.join(os.path.dirname(__file__), ''))]
sys.path[:0] = paths

from iso_simulator.building_simulator.simulator import BuildingSimulator

from iso_simulator.data_source.datasource_csv import DataSourceCSV
from iso_simulator.dibs.dibs import DIBS


def main():
    datasource = DataSourceCSV()
    building_simulator: BuildingSimulator = BuildingSimulator(DataSourceCSV(), "2004-2018", 'din', 'low')
    dibs = DIBS(datasource)

    dibs.calculate_building_result("2004-2018", 'din', 'low')


if __name__ == '__main__':
    main()

