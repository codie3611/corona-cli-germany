
import os
import tempfile
from unittest import TestCase

from corona_cli_germany.__main__ import CONSOLE, process_data


class TestMain(TestCase):

    def setUp(self) -> None:
        self.mockup_data = [
            {
                'Confirmed': 668114,
                'Deaths': 11306,
                'Recovered': 413484,
                'Active': 243324,
                'Date': '2020-11-07T00:00:00Z'
            },
            {
                'Confirmed': 682624,
                'Deaths': 11372,
                'Recovered': 421151,
                'Active': 250101,
                'Date': '2020-11-08T00:00:00Z'
            }]

    def test_processing(self):

        # ground truth printing
        # rich formatss tables
        # different on windows and linux
        desired_output = f"""
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Last Update ┃ 2020-11-08              ┃
│ New Cases   │ 14510                   │
│ Source      │ https://covid19api.com/ │
└─────────────┴─────────────────────────┘
""" if os.name != "nt" else \
            f"""
┌─────────────┬─────────────────────────┐
│ Last Update │ 2020-11-08              │
│ New Cases   │ 14510                   │
│ Source      │ https://covid19api.com/ │
└─────────────┴─────────────────────────┘
"""
        desired_output = desired_output.strip()

        # run main routine without fetching
        CONSOLE.clear()
        process_data(self.mockup_data)

        # get the printed data as string and compare
        text = CONSOLE.export_text().strip()

        self.assertEqual(text, desired_output)

    def test_saving(self):

        desired_output = """┌─────────────┬─────────────────────────┐
│ Last Update │ 2020-11-08              │
│ New Cases   │ 14510                   │
│ Source      │ https://covid19api.com/ │
└─────────────┴─────────────────────────┘

""" if os.name == "nt" else """┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Last Update ┃ 2020-11-08              ┃
│ New Cases   │ 14510                   │
│ Source      │ https://covid19api.com/ │
└─────────────┴─────────────────────────┘

"""

        with tempfile.TemporaryDirectory() as tdir:
            filepath = os.path.join(tdir, "yay")

            CONSOLE.clear()
            process_data(self.mockup_data, filepath=filepath)

            with open(filepath, "r", encoding="utf8") as fp:
                data_file = fp.read()
                self.assertEqual(data_file, desired_output)
