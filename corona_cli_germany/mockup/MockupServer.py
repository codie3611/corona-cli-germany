
import logging

from flask import Flask, jsonify


def start_mockup_server(port: int):
    """ Starts a mockup for the API server

    Parameters
    ----------
    port : int
        port to run the mockup on
    """

    # Flask Server
    app = Flask("MockupServer")

    @app.route('/country/germany')
    def handle_fetch():
        return jsonify([
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
            }
        ])

    # disable logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    app.run(port=port)
