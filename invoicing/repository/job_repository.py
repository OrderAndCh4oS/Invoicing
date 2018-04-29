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
        query = 'select id, reference_code, title, description, estimated_time, deadline from jobs where id = ?'
        self.cursor.execute(query, (id,))
        return self.get_one()

    def find_last_reference_code(self):
        self.cursor.execute(
            'select reference_code as last_reference_code from jobs where id = (select max(id) from jobs)'
        )
        return self.get_one()

    def find_jobs_by_quote_id(self, quote_id):
        query = 'select jobs.id, reference_code, jobs.title as title, description, estimated_time, status.title as status, deadline, ' \
                '(staff.first_name || \' \' || staff.last_name) as staff_name, staff.rate as rate ' \
                'from jobs ' \
                'join staff on assigned_to = staff.id ' \
                'join status on status_id = status.id ' \
                'where jobs.quote_id = ?'
        self.cursor.execute(query, (quote_id,))
        return self.get_all()

    def find_jobs_by_invoice_id(self, invoice_id):
        query = 'select jobs.id, reference_code, jobs.title as title, description, billable_time, status.title as status, deadline, ' \
                '(staff.first_name || \' \' || staff.last_name) as staff_name, staff.rate as rate ' \
                'from jobs ' \
                'join staff on assigned_to = staff.id ' \
                'join status on status_id = status.id ' \
                'where jobs.invoice_id = ?'
        self.cursor.execute(query, (invoice_id,))
        return self.get_all()

    def insert_job(self, reference_code, title, description, estimated_time, deadline, status_id, assigned_to,
                   quote_id):
        query = 'insert into jobs ' \
                '(reference_code, title, description, estimated_time, deadline, status_id, assigned_to, quote_id) ' \
                'values ' \
                '(?, ?, ?, ?, ?, ?, ?, ?)'
        self.cursor.execute(
            query,
            (reference_code, title, description, estimated_time, deadline, status_id, assigned_to, quote_id)
        )

    def update_job(self, id, reference_code, title, description, estimated_time, deadline):
        query = 'update jobs set reference_code = ?, title = ?, description = ?, estimated_time = ?, deadline = ? where id = ?'
        self.cursor.execute(query, (reference_code, title, description, estimated_time, deadline, id))

    def update_actual_time(self, id, time_spent):
        query = 'update jobs set actual_time = (actual_time + ?) where id = ?'
        self.cursor.execute(query, (time_spent, id))

    def update_billable_time(self, id, time_spent):
        query = 'update jobs set billable_time = ? where id = ?'
        self.cursor.execute(query, (time_spent, id))

    def add_to_invoice(self, id, invoice_id):
        self.cursor.execute('update jobs set invoice_id = ? where id = ?', (invoice_id, id))

    def remove_job(self, id):
        self.cursor.execute('delete from jobs where id = ?', (id,))

    def remove_jobs_by_quote_id(self, quote_id):
        self.cursor.execute('delete from jobs where quote_id = ?', (quote_id,))

    def find_jobs_by_client_id_where_complete(self, client_id):
        query = 'select jobs.id, jobs.reference_code, jobs.title, status.title as status, deadline, ' \
                '(staff.first_name || \' \' || staff.last_name) as staff_name ' \
                'from jobs ' \
                'join staff on assigned_to = staff.id ' \
                'join status on status_id = status.id ' \
                'join quotes on quote_id = quotes.id ' \
                'where quotes.client_id = ? and completed = 1'
        self.cursor.execute(query, (client_id,))
        return self.get_all()
