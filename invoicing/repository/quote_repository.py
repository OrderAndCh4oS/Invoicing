from repository.base_repository import BaseRepository


class QuoteRepository(BaseRepository):

    def find_all(self):
        query = 'select quotes.id, reference_code, date, ' \
                'clients.fullname as client_fullname, ' \
                'companies.name as company_name ' \
                'from quotes ' \
                'join clients on client_id = clients.id ' \
                'join companies on clients.company_id = companies.id'
        self.cursor.execute(query)
        return self.get_all()

    def find_by_id(self, id):
        query = 'select quotes.id, reference_code, date,  ' \
                'clients.fullname as client_fullname, ' \
                'companies.name as company_name, companies.address as company_address ' \
                'from quotes ' \
                'join clients on client_id = clients.id ' \
                'join companies on clients.company_id = companies.id ' \
                'where quotes.id = ?'
        self.cursor.execute(query, (id,))
        return self.get_one()

    def find_by_id_with_jobs(self, id):
        query = 'select quotes.id, quotes.reference_code, date,  ' \
                'clients.fullname as client_fullname, ' \
                'companies.name as company_name, companies.address as company_address, ' \
                'jobs.title as job_title, jobs.description as job_description, ' \
                'staff.rate as rate ' \
                'from quotes ' \
                'join clients on client_id = clients.id ' \
                'join companies on clients.company_id = companies.id ' \
                'join jobs on quotes.id = jobs.quote_id ' \
                'join staff on jobs.assigned_to = staff.id ' \
                'where quotes.id = ?'
        self.cursor.execute(query, (id,))
        return self.get_all()

    def find_quotes_by_client_id(self, client_id):
        self.cursor.execute('select id, reference_code, date from quotes where client_id = ?', (client_id,))
        return self.get_all()

    def find_last_reference_code(self):
        self.cursor.execute(
            'select id, reference_code as last_reference_code from quotes where id = (select max(id) from quotes)')
        return self.get_one()

    def insert_quote(self, client_id, reference_code):
        self.cursor.execute(
            "insert into quotes (client_id, reference_code, date) values (?, ?, datetime('now'))",
            (client_id, reference_code)
        )

    def update_quote(self, id, reference_code):
        self.cursor.execute('update quotes set reference_code = ? where id = ?', (reference_code, id))

    def remove_quote(self, id):
        self.cursor.execute('delete from quotes where id = ?', (id,))

    def remove_quotes_by_client_id(self, client_id):
        self.cursor.execute('delete from quotes where client_id = ?', (client_id,))
