from iso_simulator.data_source.datasource_csv import DataSourceCSV
from iso_simulator.dibs.dibs import DIBS
from iso_simulator.model.generate_data import GenerateData


def main():
    datasource = DataSourceCSV()
    dibs = DIBS(datasource)
    generate_data = GenerateData(datasource)

    # dibs.calculate_result_of_one_building('BB1002988_0_00', '2004-2018')
    # dibs.calculate_all_buildings_results(generate_data, '2004-2018')
    # dibs.parallel_mp_calculation(generate_data, '2004-2018')
    # dibs.parallel_thread_max_concurrent(generate_data, '2004-2018', 1)
    # dibs.parallel_thread_calculation(generate_data, '2004-2018')
    # dibs.parallel_process_max_concurrent(generate_data, '2004-2018', 4)
    dibs.parallel_process_calculation(generate_data, '2004-2018')
    # dibs.parallel_process_max_concurrent(generate_data, '2004-2018', 10)
    # dibs.multi(generate_data, '2004-2018')


if __name__ == '__main__':
    main()
