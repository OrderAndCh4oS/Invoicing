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
        self.add_param(param)
        self.query += 'where {} '.format(condition)
        return self

    def limit(self, limit):
        self.add_param(limit)
        self.query += 'limit ? '
        return self

    def offset(self, offset):
        self.add_param(offset)
        self.query += 'offset ? '
        return self

    def count(self):
        self.query += 'select count(*) '
        return self

    def where_id_is_last_inserted(self):
        self.query += 'where id = last_insert_rowid() '
        return self

    def and_where(self, condition, param=None):
        self.add_param(param)
        self.query += 'and {} '.format(condition)
        return self

    def join(self, table, on):
        self.query += 'join {} on {} '.format(table, on)
        return self

    def insert(self, values):
        for k, v in values.items():
            self.add_param(v)
        self.query += 'insert into {} ({}) values ({}) '.format(
            self.table,
            ', '.join([k for k in values]),
            ', '.join(['?' for _ in range(len(values))])
        )
        return self

    def update(self, set):
        for k, v in set.items():
            self.add_param(v)
        self.query = 'update {} set {} '.format(self.table, ', '.join([k + ' = ?' for k in set]))
        return self

    def delete(self, table=None):
        table = table if table else self.table
        self.query += 'delete from {} '.format(table)
        return self

    def add_param(self, param):
        if param != None:
            self.params.append(param)

    def raw(self, query, params=None):
        for param in params:
            self.add_param(param)
        self.query += query + ' '
        return self

    def build(self):
        return {'sql': self.query, 'parameters': tuple(self.params)}
