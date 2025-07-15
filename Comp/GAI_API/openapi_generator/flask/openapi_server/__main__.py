#!/usr/bin/env python3

import connexion

from openapi_server import encoder
from flask import request


def main():
    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': 'OpenAI API'},
                pythonic_params=True)

    # output log
    flask_app = app.app

    @flask_app.before_request
    def log_request_info():
        print(request)
        print(request.method, request.path)
        flask_app.logger.info(f'→ {request.method} {request.path}')

    @flask_app.after_request
    def log_response_info(response):
        print(response)
        print(response.get_data(as_text=True))

    app.run(port=5000, debug=True)


if __name__ == '__main__':
    main()
