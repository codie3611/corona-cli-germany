
from corona_cli_germany.version import get_version
import os
import sys
import tempfile
from multiprocessing import Process
from unittest import TestCase

from rich.console import Console
from rich.table import Table

from corona_cli_germany.__main__ import CONSOLE, APISettings, get_default_console, get_header, main
from corona_cli_germany.mockup.MockupServer import start_mockup_server


class TestMain(TestCase):

    def setUp(self) -> None:

        api_port = 31261

        # start mockup server
        self.app_process = Process(
            target=start_mockup_server, kwargs={"port": api_port})
        self.app_process.start()

        # mockup server address
        APISettings.URL_TEMPLATE = f"http://127.0.0.1:{api_port}/country/germany"
        "?from={from_date}&to={to_date}"

    def tearDown(self) -> None:
        if self.app_process.is_alive():
            self.app_process.terminate()

    def test_processing(self):

        # ground truth printing
        # rich formatss tables
        # different on windows and linux
        desired_output = f"""{get_header()}
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Last Update ┃ 2020-11-08              ┃
│ New Cases   │ 14510                   │
│ Source      │ https://covid19api.com/ │
└─────────────┴─────────────────────────┘""" \
    if os.name != "nt" else \
            f"""{get_header()}
┌─────────────┬─────────────────────────┐
│ Last Update │ 2020-11-08              │
│ New Cases   │ 14510                   │
│ Source      │ https://covid19api.com/ │
└─────────────┴─────────────────────────┘"""
        # set up mockup console
        console = get_default_console()
        console.print(desired_output)
        desired_output = console.export_text()

        # run main routine
        main()

        # get the printed data as string and compare
        text = CONSOLE.export_text(clear=True)

        self.assertEqual(text, desired_output)

    def test_saving(self):

        desired_output = f"""{get_header()}
┌─────────────┬─────────────────────────┐
│ Last Update │ 2020-11-08              │
│ New Cases   │ 14510                   │
│ Source      │ https://covid19api.com/ │
└─────────────┴─────────────────────────┘""" \
    if os.name == "nt" else f"""{get_header()}
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Last Update ┃ 2020-11-08              ┃
│ New Cases   │ 14510                   │
│ Source      │ https://covid19api.com/ │
└─────────────┴─────────────────────────┘"""

        # set up mockup console
        console = get_default_console()
        console.print(desired_output)
        desired_output = console.export_text()

        # run command line with storing data in tempdir
        with tempfile.TemporaryDirectory() as tdir:
            filepath = os.path.join(tdir, "yay.txt")

            sys.argv.append("--filepath")
            sys.argv.append(filepath)
            main()

            with open(filepath, "r", encoding="utf8") as fp:
                data_file = fp.read()
                self.assertEqual(data_file, desired_output)

        CONSOLE.clear()
