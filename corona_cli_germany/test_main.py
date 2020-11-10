
import sys
from unittest import TestCase

from corona_cli_germany.__main__ import CONSOLE, main, process_data
from corona_cli_germany.version import get_version


class TestMain(TestCase):

    # def setUp(self):
    #     self.server = MockupServer()
    #     self.server.start()

    #     # overwrite URL to connect to mockup
    #     APISettings.URL_TEMPLATE = APISettings.URL_TEMPLATE.replace(
    #         "https://api.covid19api.com", "http://localhost:8080")

    # def tearDown(self) -> None:
    #     self.server.stop()

    def test_process(self):

        desired_output = f"""
┌─────────────┬─────────────────────────┐
│ Last Update │ 2020-11-08              │
│ New Cases   │ 14510                   │
│ Source      │ https://covid19api.com/ │
└─────────────┴─────────────────────────┘
""".strip()

        data = [
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

        process_data(data)
        text = CONSOLE.export_text().strip()

        self.assertEqual(text, desired_output)
