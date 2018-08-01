import json

from repository.base_repository import BaseRepository
from transformer.json import JSONTransformer


class BaseAPI():

    def __init__(self, repository: BaseRepository):
        self.repository = repository

    def show_all(self):
        return JSONTransformer.resultsToJSON(self.repository.find_all(), self.repository.get_headers())

    def show_by_id(self, id):
        return JSONTransformer.resultToJSON(self.repository.find_by_id(id), self.repository.get_headers())

    def update_by_id(self, id, data):
        self.repository.update(id, json.loads(data))
        self.repository.save()
        return JSONTransformer.resultToJSON(self.repository.find_by_id(id), self.repository.get_headers())

    def add(self, data):
        self.repository.insert(json.loads(data))
        self.repository.save()
        return JSONTransformer.resultToJSON(self.repository.find_last_inserted(), self.repository.get_headers())

    def delete(self, id):
        self.repository.remove(id)
        self.repository.save()
        return json.dumps({"message": "deleted: %s" % id})
