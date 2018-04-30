from query_builder.query_builder import QueryBuilder
from repository.base_repository import BaseRepository


class InvoiceRepository(BaseRepository):

    def __init__(self):
        super().__init__('invoices')

    def find_all_join_clients_and_companies(self):
        query = QueryBuilder(self.table) \
            .select(['invoices.id', 'reference_code', 'date',
                     'clients.fullname as client_fullname',
                     'companies.name as company_name']) \
            .from_() \
            .join('clients', 'client_id = clients.id') \
            .join('companies', 'clients.company_id = companies.id')
        self.execute(**query.build())
        return self.get_all()

    def find_by_id_join_clients_and_companies(self, id):
        query = QueryBuilder(self.table) \
            .select(['invoices.id as id', 'reference_code', 'date',
                     'clients.fullname as client_fullname',
                     'companies.name as company_name', 'companies.address as company_address']) \
            .from_() \
            .join('clients', 'client_id = clients.id') \
            .join('companies', 'clients.company_id = companies.id') \
            .where('invoices.id = ?', id)
        self.execute(**query.build())
        return self.get_one()

    def find_invoices_by_client_id(self, client_id):
        query = QueryBuilder(self.table) \
            .select(['id', 'reference_code', 'date']) \
            .from_() \
            .where('client_id = ?', client_id)
        self.execute(**query.build())
        return self.get_all()

    def find_last_reference_code(self):
        query = QueryBuilder(self.table) \
            .select(['id', 'reference_code as last_reference_code']) \
            .from_() \
            .where('id = (select max(id) from invoices)')
        self.execute(**query.build())
        return self.get_one()

    def remove_invoices_by_client_id(self, client_id):
        query = QueryBuilder(self.table) \
            .delete() \
            .where('client_id = ?', client_id)
        self.execute(**query.build())
