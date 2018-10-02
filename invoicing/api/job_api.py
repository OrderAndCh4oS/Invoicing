import json
from datetime import datetime

from invoicing.api.base_api import BaseAPI
from invoicing.models.job_model import JobModel
from invoicing.repository.job_repository import JobRepository
from invoicing.transformer.json import JSONTransformer


class JobAPI(BaseAPI):

    def __init__(self):
        super().__init__(JobRepository(), JobModel())

    def add(self, data):
        self.model(**data)
        self.model.validate()
        if self.model.is_valid:
            data["reference_code"] = self.repository.make_next_reference_code()
            data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            self.repository.insert(data)
            self.repository.save()
            return JSONTransformer.resultToJSON(self.repository.find_last_inserted(), self.repository.get_headers())
        else:
            return json.dumps(self.model.get_errors())
