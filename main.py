import cProfile
import pstats

from iso_simulator.data_source.datasource_csv import DataSourceCSV
from iso_simulator.dibs.dibs import DIBS
from iso_simulator.model.generate_data import GenerateData


def main():
    datasource = DataSourceCSV()
    dibs = DIBS(datasource)
    generate_data = GenerateData(datasource, '2004-2018')

    dibs.calculate_result_of_one_building(generate_data, 'BB1002988_0_00', '2004-2018')
    # dibs.calculate_all_buildings_results(generate_data, '2004-2018')


if __name__ == '__main__':
    with cProfile.Profile() as profile:
        main()
    results = pstats.Stats(profile)
    results.sort_stats(pstats.SortKey.TIME)
    results.print_stats()
