import argparse
import datetime
import sys
from typing import Any, Dict, List

import requests
from rich.console import Console
from rich.table import Table
from rich.theme import Theme

from .version import get_version


class APISettings:
    URL_TEMPLATE = "https://api.covid19api.com/country/germany"
    "?from={from_date}&to={to_date}"

    SOURCE_PAGE = "https://covid19api.com/"


# Console
CONSOLE = Console(theme=Theme({
    "info": "blue",
    "success": "green",
    "warning": "yellow",
    "error": "bold red"
}), record=True, highlight=False)


def parse_cli_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser(
        description="Command line utility for daily corona cases in germany.",
        usage="python -m corona_cli_germany")

    parser.add_argument("--filepath",
                        type=str,
                        required=False,
                        default="",
                        help="Optional path to a file in which "
                        "the output will be saved.")

    if len(sys.argv) < 1:
        CONSOLE.print(parser.format_help())
        exit(0)

    return parser.parse_args(sys.argv[1:])


class CountryCoronaData:
    """ Class containing corona data for germany
    """
    confirmed: int = 0
    deaths: int = 0
    recovered: int = 0
    active: int = 0
    date: datetime.date


def fetch_data() -> List[dict]:
    """ Query data from the API

    Returns
    -------
    data : List[dict]
        corona API data

    Notes
    -----
        The data originates from the Corona API
        https://api.covid19api.com
    """

    today = datetime.date.today()
    a_week_ago = today - datetime.timedelta(days=3)

    url = APISettings.URL_TEMPLATE.format(
        from_date=a_week_ago.isoformat(),
        to_date=today.isoformat(),
    )

    data = requests.get(url)

    return data.json()


def parse_data(data_list: List[Dict[str, Any]]) -> List[CountryCoronaData]:
    """ Parse the corona data coming from an API

    Parameters
    ----------
    data_list : List[dict]
        list of data dictionaries each containing data from the API

    Returns
    -------
    parsed_data : List[CountryCoronaData]
        the parsed data as objects
    """

    parsed_data = []
    for data in data_list:
        country_corona_data = CountryCoronaData()

        if "Confirmed" in data:
            country_corona_data.confirmed = data["Confirmed"]

        if "Deaths" in data:
            country_corona_data.deaths = data["Deaths"]

        if "Recovered" in data:
            country_corona_data.recovered = data["Recovered"]

        if "Active" in data:
            country_corona_data.recovered = data["Active"]

        if "Date" in data:
            country_corona_data.date = datetime.date.fromisoformat(
                data["Date"][:10])

        parsed_data.append(country_corona_data)

    return parsed_data


def print_header():
    """ Prints the command line header
    """

    CONSOLE.print(
        f"""
    ┌────────┐
    │[black]Corona[/black]  │
    │[red]Germany[/red] │
    │[yellow]CLI[/yellow]     │
    ├────────┘
    │
    │ Version {get_version()}
""")


def print_data(data: List[CountryCoronaData]):
    """ Format data into a message

    Parameters
    ----------
    data: List[CountryCoronaData]
        data list used for printing
    """

    # test for enough data
    if len(data) < 2:
        msg = "[red]Received not enough data from remote server.[/red]"
        CONSOLE.print(msg)

    n_new_cases = max(data[-1].confirmed - data[-2].confirmed, 0)

    table = Table(show_header=False)
    table.add_row("Last Update", f"[black]{data[-1].date.isoformat()}[/black]")
    table.add_row("New Cases", f"[red]{n_new_cases}[/red]")
    table.add_row("Source", f"[yellow]{APISettings.SOURCE_PAGE}[/yellow]")

    CONSOLE.print(table)
    CONSOLE.print()


def process_data(data: List[dict], filepath: str = ""):
    """ Processes the data from an API

    Parameters
    ----------
    data : list
        data from the corona API
    filepath : str
        optional filepath for saving output
    """

    # parse it
    parsed_data = parse_data(data)

    # format it
    print_data(parsed_data)

    if filepath:
        CONSOLE.save_html(filepath)


def main():

    print_header()

    # get command line arguments
    args = parse_cli_args()

    # get the data
    data = fetch_data()

    # process it
    process_data(data, filepath=args.filepath)


if __name__ == "__main__":
    main()
