from iso_simulator.data_source.datasource_csv import DataSourceCSV
from iso_simulator.dibs.dibs import DIBS


def main():
    datasource = DataSourceCSV()
    dibs = DIBS(datasource)

    dibs.calculate_building_result("2004-2018", 'din18599', 'mid', 'sia2024')


if __name__ == '__main__':
    main()
