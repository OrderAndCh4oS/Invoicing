import json
import random

from repository.company_repository import CompanyRepository
from transformer.json import JSONTransformer


class CompanyAPI(CompanyRepository):

    def show_all(self):
        return JSONTransformer.resultsToJSON(self.find_all(), self.get_headers())

    def show_by_id(self, id):
        return JSONTransformer.resultToJSON(self.find_by_id(id), self.get_headers())

    def update_by_id(self, id, data):
        self.update(id, json.loads(data))
        self.save()
        return JSONTransformer.resultToJSON(self.find_by_id(id), self.get_headers())

    def add(self, data):
        self.insert(json.loads(data))
        self.save()
        return JSONTransformer.resultToJSON(self.find_last_inserted(), self.get_headers())

    def delete(self, id):
        self.remove(id)
        self.save()
        return json.dumps({"message": "deleted: %s" % id})


if __name__ == '__main__':
    api = CompanyAPI()
    print(api.show_all())
    print(api.show_by_id(1))
    names = ['A. Corp', 'Widget Co.', 'Name Ltd.', 'Someone & Sons']
    print(api.update_by_id(1, '{"name": "%s"}' % random.choice(names)))
    print(api.add('{"name": "%s", "address": "A Street"}' % random.choice(names)))
    last = api.find_last_inserted()
    print(api.delete(last['id']))
