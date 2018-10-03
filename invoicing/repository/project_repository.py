from invoicing.query_builder.query_builder import QueryBuilder
from invoicing.repository.base_repository import BaseRepository


class ProjectRepository(BaseRepository):

    def __init__(self):
        super().__init__('project')

    def find_all_join_company(self):
        query = QueryBuilder(self.table) \
            .select(['project.id', 'reference_code', 'project.title'
                     'client.fullname as client_fullname',
                     'company.name as company_name',
                     'company.id as company_id',
                     'created_at']) \
            .from_() \
            .join('company', 'company_id = company.id')
        self.execute(**query.build())
        return self.get_all()

    def find_paginated(self, limit=5, page=1, **kwargs):
        query = QueryBuilder(self.table) \
            .select(['project.id', 'project.reference_code', 'project.title',
                     'company.name as company_name',
                     'created_at',
                     ]) \
            .from_() \
            .join('company', 'company_id = company.id') \
            .limit(limit) \
            .offset(page * limit - limit)
        self.execute(**query.build())
        return self.get_all()

    def find_paginated_join_company(self, limit=5, page=1):
        query = QueryBuilder(self.table) \
            .select(['project.id', 'reference_code', 'project.title',
                     'company.name as company_name',
                     'created_at',
                     ]) \
            .from_() \
            .join('company', 'company_id = company.id') \
            .limit(limit) \
            .offset(page * limit - limit)
        self.execute(**query.build())
        return self.get_all()

    def find_by_id_join_company(self, id):
        query = QueryBuilder(self.table) \
            .select(['project.id', 'reference_code', 'project.title',
                     'company.name as company_name',
                     'company.address as company_address',
                     'created_at',
                     ]) \
            .from_() \
            .join('company', 'company_id = company.id') \
            .where('project.id = ?', id)
        self.execute(**query.build())
        return self.get_one()

    def find_by_id_with_jobs(self, id):
        query = QueryBuilder(self.table) \
            .select(['project.id', 'projects.reference_code', 'project.title',
                     'company.name as company_name',
                     'company.address as company_address',
                     'company.id as company_id',
                     'job.title as job_title',
                     'job.description as job_description',
                     'staff.rate as rate', 'created_at']) \
            .from_() \
            .join('company', 'company_id = company.id') \
            .join('job', 'project.id = job.project_id') \
            .join('staff', 'job.assigned_to = staff.id') \
            .where('project.id = ?', id)
        self.execute(**query.build())
        return self.get_all()

    def find_projects_by_company_id(self, company_id):
        query = QueryBuilder(self.table) \
            .select(['id', 'reference_code', 'title', 'created_at']) \
            .from_() \
            .where('company_id = ?', company_id)
        self.execute(**query.build())
        return self.get_all()

    def find_last_inserted_id(self):
        query = QueryBuilder(self.table) \
            .select(['id']) \
            .from_() \
            .where('id = (select max(id) from projects)')
        self.execute(**query.build())
        return self.get_one()

    def find_last_reference_code(self):
        query = QueryBuilder(self.table) \
            .select(['reference_code as last_reference_code']) \
            .from_() \
            .where('id = (select max(id) from projects)')
        self.execute(**query.build())
        return self.get_one()

    def remove_projects_by_client_id(self, client_id):
        query = QueryBuilder(self.table) \
            .delete() \
            .where('client_id = ?', client_id)
        self.execute(**query.build())
