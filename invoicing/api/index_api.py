import json

from flask import request


class IndexAPI:
    @staticmethod
    def get():
        url = request.url
        return json.dumps({
            "links": [
                url + 'company',
                url + 'client',
                url + 'staff',
                url + 'status',
                url + 'project',
                url + 'job',
                url + 'invoice'
            ]
        })
