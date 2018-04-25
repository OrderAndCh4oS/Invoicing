from repository.base_repository import BaseRepository


class JobRepository(BaseRepository):

    def find_all(self):
        query = 'select jobs.id, reference_code, jobs.title, status.title as status, deadline, ' \
                '(staff.first_name || \' \' || staff.last_name) as staff_name ' \
                'from jobs ' \
                'join staff on assigned_to = staff.id ' \
                'join status on status_id = status.id'
        self.cursor.execute(query)
        return self.get_all()

    def find_by_id(self, id):
        query = 'select id, reference_code, title, description, estimated_time from jobs where id = ?'
        self.cursor.execute(query, (id,))
        return self.get_one()

    def find_last_reference_code(self):
        self.cursor.execute(
            'select reference_code as last_reference_code from jobs where id = (select max(id) from jobs)'
        )
        return self.get_one()

    def insert_job(self, reference_code, title, description, estimated_time, deadline, status_id, assigned_to,
                   quote_id):
        query = 'insert into jobs ' \
                '(reference_code, title, description, estimated_time, deadline, status_id, assigned_to, quote_id) ' \
                'values ' \
                '(?, ?, ?, ?, ?, ?, ?, ?)'
        self.cursor.execute(query, (
        reference_code, title, description, estimated_time, deadline, status_id, assigned_to, quote_id))

    def update_job(self, reference_code, title, description, estimated_time, deadline):
        query = 'update jobs set reference_code = ?, title = ?, description = ?, estimated_time = ?, deadline = ?'
        self.cursor.execute(query, (reference_code, title, description, estimated_time, deadline))

    def remove_job(self, id):
        self.cursor.execute('delete from jobs where id = ?', (id,))

    def remove_jobs_by_quote_id(self, quote_id):
        self.cursor.execute('delete from jobs where quote_id = ?', (quote_id,))
