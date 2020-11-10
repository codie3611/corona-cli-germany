
import sys
import requests
from unittest import TestCase
import os

from corona_cli_germany.__main__ import APISettings, CONSOLE, fetch_data, main, process_data
from corona_cli_germany.version import get_version


class TestMain(TestCase):

    def test_no_connection(self):

        old_url = APISettings.URL_TEMPLATE
        APISettings.URL_TEMPLATE = "http://i_do_not_exist.wtf"
        with self.assertRaises(requests.exceptions.ConnectionError):
            fetch_data()
        APISettings.URL_TEMPLATE = old_url

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

        # run main routine without fetching
        process_data(data)

        # get the printed data as string and compare
        text = CONSOLE.export_text().strip()

        self.assertEqual(text, desired_output)
