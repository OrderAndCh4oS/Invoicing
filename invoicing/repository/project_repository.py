from query_builder.query_builder import QueryBuilder
from repository.base_repository import BaseRepository


class ProjectRepository(BaseRepository):

    def __init__(self):
        super().__init__('projects')

    def find_all_join_clients_and_company(self):
        query = QueryBuilder(self.table) \
            .select(['projects.id', 'reference_code', 'date',
                     'clients.fullname as client_fullname',
                     'companies.name as company_name']) \
            .from_() \
            .join('clients', 'client_id = clients.id') \
            .join('companies', 'clients.company_id = companies.id')
        self.execute(**query.build())
        return self.get_all()

    def find_by_id_join_clients_and_company(self, id):
        query = QueryBuilder(self.table) \
            .select(['projects.id', 'reference_code', 'date',
                     'clients.fullname as client_fullname',
                     'companies.name as company_name', 'companies.address as company_address']) \
            .from_() \
            .join('clients', 'client_id = clients.id') \
            .join('companies', 'clients.company_id = companies.id') \
            .where('projects.id = ?', id)
        self.execute(**query.build())
        return self.get_one()

    def find_by_id_with_jobs(self, id):
        query = QueryBuilder(self.table) \
            .select(['projects.id', 'projects.reference_code', 'date',
                     'clients.fullname as client_fullname',
                     'companies.name as company_name',
                     'companies.address as company_address',
                     'jobs.title as job_title',
                     'jobs.description as job_description',
                     'staff.rate as rate']) \
            .from_() \
            .join('clients', 'client_id = clients.id') \
            .join('companies', 'clients.company_id = companies.id') \
            .join('jobs', 'projects.id = jobs.project_id') \
            .join('staff', 'jobs.assigned_to = staff.id') \
            .where('projects.id = ?', id)
        self.execute(**query.build())
        return self.get_all()

    def find_projects_by_client_id(self, client_id):
        query = QueryBuilder(self.table) \
            .select(['id', 'reference_code', 'date']) \
            .from_() \
            .where('client_id = ?', client_id)
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

    def make_next_reference_code(self):
        last_project = self.find_last_reference_code()
        last_reference_code = last_project["last_reference_code"] if last_project else 'P-1000'
        reference_code = 'P-' + str(int(last_reference_code[2:]) + 1)
        return reference_code

    def remove_projects_by_client_id(self, client_id):
        query = QueryBuilder(self.table) \
            .delete() \
            .where('client_id = ?', client_id)
        self.execute(**query.build())
