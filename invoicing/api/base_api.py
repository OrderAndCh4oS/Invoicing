from models.base_model import BaseModel
from repository.base_repository import BaseRepository
from transformer.json import JSONTransformer


class BaseAPI():

    def __init__(self, repository: BaseRepository, model: BaseModel):
        self.model = model
        self.repository = repository

    def show_all(self):
        return JSONTransformer.resultsToJSON(self.repository.find_all(), self.repository.get_headers())

    def show_by_id(self, id):
        return JSONTransformer.resultToJSON(self.repository.find_by_id(id), self.repository.get_headers())

    def update_by_id(self, id, data):
        self.model(**data)
        self.model.validate()
        if self.model.is_valid:
            self.repository.update(id, data)
            self.repository.save()
            return JSONTransformer.resultToJSON(self.repository.find_by_id(id), self.repository.get_headers())
        else:
            return JSONTransformer.errorToJSON(self.model.get_errors())

    def add(self, data):
        self.model(**data)
        self.model.validate()
        if self.model.is_valid:
            self.repository.insert(data)
            self.repository.save()
            return JSONTransformer.resultToJSON(self.repository.find_last_inserted(), self.repository.get_headers())
        else:
            return JSONTransformer.errorToJSON(self.model.get_errors())

    def delete(self, id):
        self.repository.remove(id)
        self.repository.save()
        return JSONTransformer.messageToJSON("deleted: %s" % id)
