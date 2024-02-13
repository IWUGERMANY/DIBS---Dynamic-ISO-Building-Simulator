import os
import typer
from rich.console import Console
from rich.table import Table
from iso_simulator.data_source.datasource_csv import DataSourceCSV
from iso_simulator.dibs.dibs import DIBS
from validate_inputs import (
    validate_profile_from_norm,
    validate_gains_from_group_values,
    validate_usage_from_norm,
    validate_weather_period,
    get_user_arguments,
    check_the_file_given_by_the_user,
    UNITS,
)

console = Console()
app = typer.Typer()


@app.command(
    short_help="Simulate one building which means that the given file must contain just one building"
)
def simulate_one_building(
    path: str,
    profile_from_norm: str = typer.Argument(
        "din18599", callback=validate_profile_from_norm, help="Choose a profile from"
    ),
    gains_from_group_values: str = typer.Argument(
        "mid", callback=validate_gains_from_group_values, help="Choose a gain from"
    ),
    usage_from_norm: str = typer.Argument(
        "sia2024", callback=validate_usage_from_norm, help="Choose a usage norm from"
    ),
    weather_period: str = typer.Argument(
        "2007-2021",
        callback=validate_weather_period,
        help="Invalid date range format. Please use 'YYYY-YYYY'.",
    ),
):
    user_args = get_user_arguments(
        gains_from_group_values, profile_from_norm, usage_from_norm, weather_period
    )

    check_the_file_given_by_the_user(path)

    datasource_csv = DataSourceCSV()

    dibs = DIBS(datasource_csv)
    (
        result_data_frame,
        building_id,
        simulation_time,
        excel_time,
        csv_time,
        excel_file_name,
        csv_file_name,
    ) = dibs.calculate_result_of_one_building(path, user_args)

    console.print(
        f"Time to simulate the [bold yellow]building[/bold yellow] with the id [bold yellow]{building_id}.csv[/bold yellow] is : [bold magenta]{simulation_time}s[/bold magenta]"
    )

    console.print(
        f"Time to save [bold yellow]results of the 8760 hours[/bold yellow] in [bold yellow]Excel[/bold yellow] file is : [bold magenta]{excel_time}s[/bold magenta]"
    )

    console.print(
        f"Time to save [bold yellow]results[/bold yellow] in [bold yellow]csv[/bold yellow] file is : [bold magenta]{csv_time}s[/bold magenta]"
    )

    console.print(
        f"The files contain the results are [bold yellow]{excel_file_name}[/bold yellow] and [bold yellow]{csv_file_name}[/bold yellow] and saved in this folder [bold magenta]{os.path.dirname(path)}[/bold magenta]"
    )

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=6)
    table.add_column("FEATURE", min_width=20)
    table.add_column("VALUE", min_width=13)
    table.add_column("UNIT", width=10)

    for index, (column_name, series) in enumerate(result_data_frame.items()):
        table.add_row(
            str(index),
            column_name,
            f"[bold magenta]{str(series.iloc[0])}[/bold magenta]",
            f'[bold cyan]{UNITS[index].replace("[", "").replace("]", "")}[/bold cyan]',
        )

    console.print(table)


@app.command(short_help="Simulate all building")
def simulate_all_building(
    path: str,
    profile_from_norm: str = typer.Argument(
        "din18599", callback=validate_profile_from_norm, help="Choose a profile from"
    ),
    gains_from_group_values: str = typer.Argument(
        "mid", callback=validate_gains_from_group_values, help="Choose a gain from"
    ),
    usage_from_norm: str = typer.Argument(
        "sia2024", callback=validate_usage_from_norm, help="Choose a usage norm from"
    ),
    weather_period: str = typer.Argument(
        "2007-2021",
        callback=validate_weather_period,
        help="Invalid date range format. Please use 'YYYY-YYYY'.",
    ),
):
    user_args = get_user_arguments(
        gains_from_group_values, profile_from_norm, usage_from_norm, weather_period
    )

    check_the_file_given_by_the_user(path)

    datasource_csv = DataSourceCSV()

    dibs = DIBS(datasource_csv)

    get_user_buildings = datasource_csv.get_user_buildings(path)

    simulation_time, excel_time, saving_time, folder_path = dibs.multi(
        get_user_buildings, path, user_args
    )

    console.print(
        "---------------------------------------------------------------------------------"
    )
    console.print(
        f"All results will be saved in the folder: [bold magenta]{folder_path}s[/bold magenta]"
    )
    console.print(
        "---------------------------------------------------------------------------------"
    )
    console.print(
        f"Time to simulate all buildings is: [bold magenta]{simulation_time}s[/bold magenta]"
    )
    console.print(
        f"Time to save results Excel file is: [bold gold]{excel_time}s[/bold gold]"
    )
    console.print(
        f"Time to simulate all buildings is: [bold yellow]{saving_time}s[/bold yellow]"
    )


if __name__ == "__main__":
    app()
