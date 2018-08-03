import json


class IndexAPI:
    @staticmethod
    def get():
        return json.dumps({
            "routes": [
                'http://localhost:5000/company',
                'http://localhost:5000/client',
                'http://localhost:5000/staff',
                'http://localhost:5000/status',
                'http://localhost:5000/project',
                'http://localhost:5000/job',
                'http://localhost:5000/invoice'
            ]
        })
