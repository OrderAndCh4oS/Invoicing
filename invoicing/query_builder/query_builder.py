class QueryBuilder:
    def __init__(self, table):
        self.table = table
        self.query = ''
        self.params = []

    def select(self, params):
        self.query += 'select {} '.format(', '.join(params))
        return self

    def from_(self, table=None):
        table = table if table else self.table
        self.query += 'from {} '.format(table)
        return self

    def where(self, condition, param=None):
        self.addParam(param)
        self.query += 'where {} '.format(condition)
        return self

    def andWhere(self, condition, param=None):
        self.addParam(param)
        self.query += 'and {} '.format(condition)
        return self

    def join(self, table, on):
        self.query += 'join {} on {} '.format(table, on)
        return self

    def insert(self, values):
        for k, v in values.items():
            self.addParam(v)
        self.query += 'insert into {} ({}) values ({}) '.format(
            self.table,
            ', '.join([k for k in values]),
            ', '.join(['?' for _ in range(len(values))])
        )
        return self

    def update(self, set):
        for k, v in set.items():
            self.addParam(v)
        self.query = 'update {} set {} '.format(self.table, ', '.join([k + ' = ?' for k in set]))
        return self

    def delete(self, table=None):
        table = table if table else self.table
        self.query += 'delete from {} '.format(table)
        return self

    def addParam(self, param):
        if param != None:
            self.params.append(param)

    def raw(self, query, params=None):
        for param in params:
            self.addParam(param)
        self.query += query + ' '
        return self

    def build(self):
        print(self.query)
        return {'sql': self.query, 'parameters': tuple(self.params)}
