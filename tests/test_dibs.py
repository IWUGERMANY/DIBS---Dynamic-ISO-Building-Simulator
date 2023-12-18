from iso_simulator.dibs.dibs import DIBS
from iso_simulator.data_source.datasource_csv import DataSourceCSV

class TestDibs:
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.dibs = DIBS(DataSourceCSV())

    # def test_calc_energy_demand_for_time_step_hour0(self):
