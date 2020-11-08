import rich
from rich.table import Table
import datetime
from typing import Any, Dict, List
import requests

# API
URL_TEMPLATE = "https://api.covid19api.com/country/germany?from={from_date}&to={to_date}"
SOURCE_PAGE = "https://covid19api.com/"


class CountryCoronaData:
    """ Class containing corona data for germany
    """
    confirmed: int = 0
    deaths: int = 0
    recovered: int = 0
    active: int = 0
    date: datetime.date


def fetch_data() -> list:
    """ Query data from the API

    Returns
    -------
    data : dict
        corona API data

    Notes
    -----
        The data originates from the Corona API
        https://api.covid19api.com
    """

    today = datetime.date.today()
    a_week_ago = today - datetime.timedelta(days=7)

    url = URL_TEMPLATE.format(
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

    rich.print("""
              ┌────────────┐
    [black]Corona[/black]    │ [on black]           [/on black]│
    [red]Germany[/red]   │ [on #d60000]           [/on #d60000]│
    [yellow]CLI[/yellow]       │ [on #ffce00]           [/on #ffce00]│
              └────────────┘
    """)


def print_data(data: List[CountryCoronaData]):
    """ Format data into a message

    Parameters
    ----------
    data : List[CountryCoronaData]
        data list used for printing
    """

    # test for enough data
    if len(data) < 2:
        msg = "[red]Error: Received not enough data from remote server.[/red]"
        rich.print(msg)

    n_new_cases = max(data[-1].confirmed - data[-2].confirmed, 0)

    table = Table(show_header=False)
    table.add_row("Last Update", f"[black]{data[-1].date.isoformat()}[/black]")
    table.add_row("New Cases", f"[red]{n_new_cases}[/red]")
    table.add_row("Source", f"[yellow]{SOURCE_PAGE}[/yellow]")

    rich.print(table)
    print()


def main():

    print_header()

    # get the data
    data = fetch_data()

    # parse it
    parsed_data = parse_data(data)

    # format it
    print_data(parsed_data)


if __name__ == "__main__":
    main()
