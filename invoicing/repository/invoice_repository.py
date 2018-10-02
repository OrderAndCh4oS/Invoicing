from invoicing.query_builder.query_builder import QueryBuilder
from invoicing.repository.base_repository import BaseRepository


class InvoiceRepository(BaseRepository):

    def __init__(self):
        super().__init__('invoice')

    def find_all_join_clients_and_companies(self):
        query = QueryBuilder(self.table) \
            .select(['invoice.id', 'reference_code', 'created_at',
                     'client.fullname as client_fullname',
                     'company.name as company_name']) \
            .from_() \
            .join('client', 'client_id = client.id') \
            .join('company', 'client.company_id = company.id')
        self.execute(**query.build())
        return self.get_all()

    def find_paginated_join_clients_and_companies(self, limit=5, page=1):
        query = QueryBuilder(self.table) \
            .select(['invoice.id', 'reference_code', 'created_at',
                     'client.id as client_id, client.fullname as client_fullname',
                     'company.name as company_name']) \
            .from_() \
            .join('client', 'client_id = client.id') \
            .join('company', 'client.company_id = company.id') \
            .limit(limit) \
            .offset(page * limit - limit)
        self.execute(**query.build())
        return self.get_all()

    def find_by_id_join_clients_and_companies(self, id):
        query = QueryBuilder(self.table) \
            .select(['invoice.id as id', 'reference_code', 'created_at',
                     'client.id as client_id, client.fullname as client_fullname',
                     'company.name as company_name', 'company.address as company_address']) \
            .from_() \
            .join('client', 'client_id = client.id') \
            .join('company', 'client.company_id = company.id') \
            .where('invoice.id = ?', id)
        self.execute(**query.build())
        return self.get_one()

    def find_invoices_by_client_id(self, client_id):
        query = QueryBuilder(self.table) \
            .select(['id', 'reference_code', 'created_at']) \
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
