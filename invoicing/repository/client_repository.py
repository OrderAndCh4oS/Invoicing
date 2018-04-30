from query_builder.query_builder import QueryBuilder
from repository.base_repository import BaseRepository


class ClientRepository(BaseRepository):

    def __init__(self):
        super().__init__('clients')

    def find_all_join_companies(self):
        query = QueryBuilder(self.table) \
            .select(['clients.id', 'fullname', 'email', 'telephone', 'companies.name as company_name']) \
            .from_() \
            .join('companies', 'company_id = companies.id')
        self.execute(**query.build())
        return self.get_all()

    def find_by_id_join_company(self, id):
        query = QueryBuilder(self.table) \
            .select(['clients.id', 'fullname', 'email', 'telephone',
                     'companies.name as company_name',
                     'companies.address as company_address']) \
            .from_() \
            .join('companies', 'company_id = companies.id') \
            .where('clients.id = ?', id)
        self.execute(**query.build())
        return self.get_one()

    def find_clients_by_company_id(self, company_id):
        query = QueryBuilder(self.table) \
            .select(['id', 'fullname', 'email', 'telephone', 'company_id']) \
            .from_() \
            .where('company_id = ?', company_id)
        self.execute(**query.build())
        return self.get_all()

    def find_client_and_company_by_id(self, id):
        query = QueryBuilder(self.table) \
            .select(['id', 'fullname', 'email', 'telephone', 'name', 'address']) \
            .from_() \
            .join('company', 'client.company_id = company.id') \
            .where('client.id = ?', id)
        self.execute(**query.build())
        return self.get_one()

    def remove_clients_by_company_id(self, company_id):
        query = QueryBuilder(self.table) \
            .delete() \
            .where('company_id = ?', company_id)
        self.execute(**query.build())
