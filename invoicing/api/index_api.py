import json


class IndexAPI:
    @staticmethod
    def get():
        return json.dumps({
            "routes": [
                '/company',
                '/client',
                '/staff',
                '/status',
                '/project',
                '/job',
                '/invoice'
            ]
        })
