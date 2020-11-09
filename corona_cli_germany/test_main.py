
import sys
from unittest import TestCase

from corona_cli_germany.__main__ import CONSOLE, main


class TestMain(TestCase):

    # def setUp(self):
    #     self.server = MockupServer()
    #     self.server.start()

    #     # overwrite URL to connect to mockup
    #     APISettings.URL_TEMPLATE = APISettings.URL_TEMPLATE.replace(
    #         "https://api.covid19api.com", "http://localhost:8080")

    # def tearDown(self) -> None:
    #     self.server.stop()

    def test_main(self):

        desired_output = r"""
    ┌────────┐
    │Corona  │
    │Germany │
    │CLI     │
    ├────────┘
    │
    │ Version 1.0.0

┌─────────────┬─────────────────────────┐
│ Last Update │ 2020-11-08              │
│ New Cases   │ 14510                   │
│ Source      │ https://covid19api.com/ │
└─────────────┴─────────────────────────┘
""".strip()

        sys.argv = ["__main__.py"]
        main()
        text = CONSOLE.export_text().strip()

        self.assertEqual(text, desired_output)
