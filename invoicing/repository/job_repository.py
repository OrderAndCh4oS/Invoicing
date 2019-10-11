from invoicing.query_builder.query_builder import QueryBuilder
from invoicing.repository.base_repository import BaseRepository


class JobRepository(BaseRepository):

    def __init__(self):
        super().__init__('job')

    def find_all_join_staff_and_status(self):
        query = QueryBuilder(self.table) \
            .select(['job.id', 'reference_code', 'job.title', 'status.title as status', 'deadline',
                     '(staff.first_name || \' \' || staff.last_name) as assigned_to',
                     'created_at', 'completed']) \
            .from_() \
            .join('staff', 'assigned_to = staff.id') \
            .join('status', 'status_id = status.id')
        self.execute(**query.build())
        return self.get_all()

    def find_paginated_join_staff_and_status(self, limit=5, page=1):
        query = QueryBuilder(self.table) \
            .select(['job.id', 'reference_code', 'job.title', 'status.title as status', 'deadline',
                     '(staff.first_name || \' \' || staff.last_name) as assigned_to',
                     'created_at', 'completed']) \
            .from_() \
            .join('staff', 'assigned_to = staff.id') \
            .join('status', 'status_id = status.id') \
            .limit(limit) \
            .offset(page * limit - limit)
        self.execute(**query.build())
        return self.get_all()

    def find_by_assigned_to(self, staff_id):
        query = QueryBuilder(self.table) \
            .select(['job.id', 'reference_code', 'job.title', 'description', 'estimated_time', 'actual_time',
                     'status.title as status', 'deadline']) \
            .from_() \
            .join('status', 'status_id = status.id') \
            .where('assigned_to = ?', staff_id)
        self.execute(**query.build())
        return self.get_all()

    def find_paginated_by_assigned_to(self, staff_id, limit=5, page=1):
        query = QueryBuilder(self.table) \
            .select(['job.id', 'reference_code', 'job.title', 'description', 'estimated_time', 'actual_time',
                     'status.title as status', 'deadline']) \
            .from_() \
            .join('status', 'status_id = status.id') \
            .where('assigned_to = ?', staff_id) \
            .limit(limit) \
            .offset(page * limit - limit)
        self.execute(**query.build())
        return self.get_all()

    def find_jobs_by_project_id(self, project_id):
        query = QueryBuilder(self.table) \
            .select(['job.id', 'reference_code', 'job.title as title', 'description', 'estimated_time',
                     'status.title as status', 'deadline',
                     '(staff.first_name || \' \' || staff.last_name) as staff_name', 'staff.rate as rate']) \
            .from_() \
            .join('staff', 'assigned_to = staff.id') \
            .join('status', 'status_id = status.id') \
            .where('job.project_id = ?', project_id)
        self.execute(**query.build())
        return self.get_all()

    def find_jobs_by_invoice_id(self, invoice_id):
        query = QueryBuilder(self.table) \
            .select(
            ['job.id', 'reference_code', 'job.title as title', 'description', 'billable_time', 'estimated_time',
             'actual_time',
                     'status.title as status', 'deadline',
                     '(staff.first_name || \' \' || staff.last_name) as staff_name', 'staff.rate as rate']) \
            .from_() \
            .join('staff', 'assigned_to = staff.id') \
            .join('status', 'status_id = status.id') \
            .where('job.invoice_id = ?', invoice_id)
        self.execute(**query.build())
        return self.get_all()

    def find_jobs_by_client_id_where_complete(self, client_id):
        query = QueryBuilder(self.table) \
            .select(['job.id', 'job.reference_code', 'job.title',
                     'status.title as status', 'deadline',
                     '(staff.first_name || \' \' || staff.last_name) as staff_name']) \
            .from_() \
            .join('staff', 'assigned_to = staff.id') \
            .join('status', 'status_id = status.id') \
            .join('project', 'project_id = project.id') \
            .where('project.client_id = ?', client_id) \
            .and_where('completed = ?', '1')
        self.execute(**query.build())
        return self.get_all()

    def find_paginated_jobs_by_client_id_where_not_complete(self, client_id, limit=5, page=1):
        query = QueryBuilder(self.table) \
            .select(['job.id', 'job.reference_code', 'job.title',
                     'status.title as status', 'deadline',
                     '(staff.first_name || \' \' || staff.last_name) as staff_name']) \
            .from_() \
            .join('staff', 'assigned_to = staff.id') \
            .join('status', 'status_id = status.id') \
            .join('project', 'project_id = project.id') \
            .where('project.client_id = ?', client_id) \
            .and_where('completed = ?', '0') \
            .limit(limit) \
            .offset(limit * page - limit)
        self.execute(**query.build())
        return self.get_all()

    def find_last_reference_code(self):
        query = QueryBuilder(self.table) \
            .select(['reference_code as last_reference_code']) \
            .from_() \
            .where('id = (select max(id) from job)')
        self.execute(**query.build())
        return self.get_one()

    def make_next_reference_code(self):
        last_job = self.find_last_reference_code()
        last_reference_code = last_job['last_reference_code'] if last_job else 'J-1000'
        reference_code = 'J-' + str(int(last_reference_code[2:]) + 1)
        return reference_code

    def update_actual_time(self, id, time_spent):
        query = QueryBuilder(self.table) \
            .raw('update job set actual_time = (actual_time + ?) where id = ?', (time_spent, id))
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

    def remove_jobs_by_project_id(self, project_id):
        query = QueryBuilder(self.table) \
            .delete() \
            .where('project_id = ?', project_id)
        self.execute(**query.build())

    def remove_jobs_by_invoice_id(self, invoice_id):
        query = QueryBuilder(self.table) \
            .delete() \
            .where('invoice_id = ?', invoice_id)
        self.execute(**query.build())
