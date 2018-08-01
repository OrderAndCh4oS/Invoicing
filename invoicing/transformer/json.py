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
        return json.dumps(results)

    @staticmethod
    def resultToJSON(row, headers):
        result = {}
        for i, header in enumerate(headers):
            result[header] = row[i]
        return json.dumps(result)
