class BaseRelationship:
    def __init__(self, name, repository, model, paginated_menu=None):
        self.name = name
        self.repository = repository
        self.model = model
        self.paginated_menu = paginated_menu


class OneToManyRelationship(BaseRelationship):
    def __init__(self, related_name, name, repository, model, paginated_menu=None):
        super().__init__(name, repository, model, paginated_menu)
        self.related_name = related_name
