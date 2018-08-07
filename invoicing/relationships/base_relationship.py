class BaseRelationship:
    def __init__(self, name, repository, model):
        self.name = name
        self.repository = repository
        self.model = model


class OneToManyRelationship(BaseRelationship):
    def __init__(self, related_name, name, repository, model):
        super().__init__(name, repository, model)
        self.related_name = related_name
