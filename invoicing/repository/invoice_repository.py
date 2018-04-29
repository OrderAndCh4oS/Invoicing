from repository.base_repository import BaseRepository


class InvoiceRepository(BaseRepository):

    def find_all(self):
        query = 'select invoices.id, reference_code, date, ' \
                'clients.fullname as client_fullname, ' \
                'companies.name as company_name ' \
                'from invoices ' \
                'join clients on client_id = clients.id ' \
                'join companies on clients.company_id = companies.id'
        self.cursor.execute(query)
        return self.get_all()

    def find_by_id(self, id):
        query = 'select invoices.id as id, reference_code, date,  ' \
                'clients.fullname as client_fullname, ' \
                'companies.name as company_name, companies.address as company_address ' \
                'from invoices ' \
                'join clients on client_id = clients.id ' \
                'join companies on clients.company_id = companies.id ' \
                'where invoices.id = ?'
        self.cursor.execute(query, (id,))
        return self.get_one()

    def find_invoices_by_client_id(self, client_id):
        self.cursor.execute('select id, reference_code, date from invoices where client_id = ?', (client_id,))
        return self.get_all()

    def find_last_reference_code(self):
        self.cursor.execute(
            'select id, reference_code as last_reference_code from invoices where id = (select max(id) from invoices)')
        return self.get_one()

    def insert_invoice(self, client_id, reference_code):
        self.cursor.execute(
            "insert into invoices (client_id, reference_code, date) values (?, ?, datetime('now'))",
            (client_id, reference_code)
        )

    def update_invoice(self, id, reference_code):
        self.cursor.execute('update invoices set reference_code = ? where id = ?', (reference_code, id))

    def remove_invoice(self, id):
        self.cursor.execute('delete from invoices where id = ?', (id,))

    def remove_invoices_by_client_id(self, client_id):
        self.cursor.execute('delete from invoices where client_id = ?', (client_id,))
