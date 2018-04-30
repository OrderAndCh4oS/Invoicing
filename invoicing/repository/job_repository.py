from query_builder.query_builder import QueryBuilder
from repository.base_repository import BaseRepository


class JobRepository(BaseRepository):

    def __init__(self):
        super().__init__('jobs')

    def find_all_join_staff_and_status(self):
        query = QueryBuilder(self.table) \
            .select(['jobs.id', 'reference_code', 'jobs.title', 'status.title as status', 'deadline',
                     '(staff.first_name || \' \' || staff.last_name) as assigned_to']) \
            .from_() \
            .join('staff', 'assigned_to = staff.id') \
            .join('status', 'status_id = status.id')
        self.execute(**query.build())
        return self.get_all()

    def find_by_assigned_to(self, staff_id):
        query = QueryBuilder(self.table) \
            .select(['jobs.id', 'reference_code', 'jobs.title', 'description', 'estimated_time', 'actual_time',
                     'status.title as status', 'deadline']) \
            .from_() \
            .join('status', 'status_id = status.id') \
            .where('assigned_to = ?', staff_id)
        self.execute(**query.build())
        return self.get_all()

    def find_last_reference_code(self):
        query = QueryBuilder(self.table) \
            .select(['reference_code as last_reference_code']) \
            .from_() \
            .where('id = (select max(id) from jobs)')
        self.execute(**query.build())
        return self.get_one()

    def find_jobs_by_quote_id(self, quote_id):
        query = QueryBuilder(self.table) \
            .select(['jobs.id', 'reference_code', 'jobs.title as title', 'description', 'estimated_time',
                     'status.title as status', 'deadline',
                     '(staff.first_name || \' \' || staff.last_name) as staff_name', 'staff.rate as rate']) \
            .from_() \
            .join('staff', 'assigned_to = staff.id') \
            .join('status', 'status_id = status.id') \
            .where('jobs.quote_id = ?', quote_id)
        self.execute(**query.build())
        return self.get_all()

    def find_jobs_by_invoice_id(self, invoice_id):
        query = QueryBuilder(self.table) \
            .select(['jobs.id', 'reference_code', 'jobs.title as title', 'description', 'billable_time',
                     'status.title as status', 'deadline',
                     '(staff.first_name || \' \' || staff.last_name) as staff_name', 'staff.rate as rate']) \
            .from_() \
            .join('staff', 'assigned_to = staff.id') \
            .join('status', 'status_id = status.id') \
            .where('jobs.invoice_id = ?', invoice_id)
        self.execute(**query.build())
        return self.get_all()

    def find_jobs_by_client_id_where_complete(self, client_id):
        query = QueryBuilder(self.table) \
            .select(['jobs.id', 'jobs.reference_code', 'jobs.title',
                     'status.title as status', 'deadline',
                     '(staff.first_name || \' \' || staff.last_name) as staff_name']) \
            .from_() \
            .join('staff', 'assigned_to = staff.id') \
            .join('status', 'status_id = status.id') \
            .join('quotes', 'quote_id = quotes.id') \
            .where('quotes.client_id = ?', client_id) \
            .andWhere('completed = ?', '1')
        self.execute(**query.build())
        return self.get_all()

    def update_actual_time(self, id, time_spent):
        query = QueryBuilder(self.table) \
            .raw('update jobs set actual_time = (actual_time + ?) where id = ?', (time_spent, id))
        self.execute(**query.build())

    def update_billable_time(self, id, time_spent):
        query = QueryBuilder(self.table) \
            .update({'billable_time': time_spent}) \
            .where('id = ?', id)
        self.execute(**query.build())

    def update_mark_as_complete(self, id):
        query = QueryBuilder(self.table) \
            .update({'completed': 1}) \
            .where('id = ?', id)
        self.execute(**query.build())

    def add_to_invoice(self, id, invoice_id):
        query = QueryBuilder(self.table) \
            .update({'invoice_id': invoice_id}) \
            .where('id = ?', id)
        self.execute(**query.build())

    def remove_jobs_by_quote_id(self, quote_id):
        query = QueryBuilder(self.table) \
            .delete() \
            .where('quote_id = ?', quote_id)
        self.execute(**query.build())

    def remove_jobs_by_invoice_id(self, invoice_id):
        query = QueryBuilder(self.table) \
            .delete() \
            .where('invoice_id = ?', invoice_id)
        self.execute(**query.build())
