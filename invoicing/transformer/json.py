import json


class JSONTransformer:
    @staticmethod
    def resultsToJSON(rows, headers):
        results = []
        for row in rows:
            data = {}
            for i, header in enumerate(headers):
                data[header] = row[i]
            results.append(data)
        return JSONTransformer.dataToJSON(results)

    @staticmethod
    def resultToJSON(row, headers):
        result = {}
        for i, header in enumerate(headers):
            result[header] = row[i]
        return JSONTransformer.dataToJSON(result)

    @staticmethod
    def dataToJSON(data):
        response = {
            "data": data
        }
        return json.dumps(response)

    @staticmethod
    def errorToJSON(errors):
        response = {
            "errors": errors
        }
        return json.dumps(response)

    @staticmethod
    def messageToJSON(message):
        response = {
            "message": message
        }
        return json.dumps(response)
