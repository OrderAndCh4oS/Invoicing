import datetime

from actions.action import Action
from crud.base_crud import BaseCrud
from crud.job_crud import JobCrud
from latex.latex_quote import LatexQuote
from repository.client_repository import ClientRepository
from repository.job_repository import JobRepository
from repository.quote_repository import QuoteRepository
from ui.date import Date
from ui.menu import Menu
from ui.style import Style


class QuoteCrud(BaseCrud, QuoteRepository):
    def __init__(self):
        super().__init__('Quotes')
        super(QuoteRepository, self).__init__('quotes')

    def menu(self):
        title = Style.create_title('Manage ' + self.table_name)
        actions = [
            Action('1', 'View', self.show),
            Action('2', 'Add', self.add),
            Action('3', 'Edit', self.edit),
            Action('4', 'Delete', self.delete),
            Action('5', 'Generate', self.generate),
            Action('b', 'Back', False)
        ]
        Menu.create(title, actions)

    def show(self):
        print(Style.create_title('Show Quote'))
        quote = Menu.select_row_by(
            self.find_all_join_clients_and_company,
            self.cursor,
            self.find_by_id_join_clients_and_company
        )
        if quote:
            print(Style.create_title('Quote Data'))
            print('Company: ' + quote['company_name'])
            print('Client: ' + quote['client_fullname'])
            print('Date: ' + quote['date'])
            print('Reference Code: ' + quote['reference_code'])
            # Todo: print quote items
            Menu.waitForInput()

    def add(self):
        print(Style.create_title('Add Quote'))
        client = Menu.select_row(ClientRepository(), 'Select Client')
        last_quote = self.find_last_reference_code()
        last_reference_code = last_quote["last_reference_code"] if last_quote else 'Q-7000'
        reference_code = 'Q-' + str(int(last_reference_code[2:]) + 1)
        if client and len(reference_code) > 0:
            self.insert({
                'client_id': client['id'],
                'reference_code': reference_code,
                'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            self.save()
            self.check_rows_updated('Quote Added')
            self.add_jobs()
            print('Quote added')
        else:
            print('Quote not added')
        Menu.waitForInput()

    def add_jobs(self):
        while True:
            add_job = Menu.yes_no_question('Add job')
            if add_job == 'n':
                break
            elif add_job != 'y' and add_job != 'Y' and add_job != '':
                continue
            JobCrud().add()

    def edit(self):
        print(Style.create_title('Edit Quote'))
        quote = Menu.select_row_by(
            self.find_all_join_clients_and_company,
            self.cursor,
            self.find_by_id_join_clients_and_company
        )
        if quote:
            reference_code = self.update_field(quote['reference_code'], 'Reference Code')
            self.update(quote['id'], {'reference_code': reference_code})
            self.save()
            self.check_rows_updated('Quote Updated')
            self.add_jobs()
            Menu.waitForInput()

    def generate(self):
        print(Style.create_title('Generate Quote'))
        quote = Menu.select_row_by(
            self.find_all_join_clients_and_company,
            self.cursor,
            self.find_by_id_join_clients_and_company
        )
        if quote:
            jobs = JobRepository().find_jobs_by_quote_id(quote['id'])
            quote_data = {
                'reference_code': quote['reference_code'],
                'company_name': quote['company_name'],
                'company_address': quote['company_address'],
                'date': Date().convert_date_time_for_printing(quote['date']),
                'total_cost': '£' + str(sum([float(job['rate']) * float(job['estimated_time']) for job in jobs])),
                'jobs': [{
                    'title': job['title'],
                    'description': job['description'],
                    'type': 'hours',
                    'estimated_time': str(job['estimated_time']),
                    'staff_rate': '£' + str(job['rate']),
                    'cost': '£' + str(float(job['rate']) * float(job['estimated_time']))
                } for job in jobs]
            }
            LatexQuote().generate(**quote_data)
            Menu.waitForInput()

    def delete(self):
        print(Style.create_title('Delete Quote'))
        quote = Menu.select_row_by(
            self.find_all_join_clients_and_company,
            self.cursor,
            self.find_by_id_join_clients_and_company
        )
        if quote:
            user_action = False
            while not user_action == 'delete':
                user_action = input('Type \'delete\' to remove this quote or \'c\' to cancel: ')
                if user_action == 'c':
                    return
            if user_action == 'delete':
                self.remove_children(quote['id'])
                self.remove(quote['id'])
                self.save()
                self.check_rows_updated('Quote Deleted')
                Menu.waitForInput()

    def delete_quotes_by_client_id(self, client_id):
        quotes = self.find_quotes_by_client_id(client_id)
        for quote in quotes:
            self.remove_children(quote['id'])
        self.remove_quotes_by_client_id(client_id)
        self.save()

    def remove_children(self, quote_id):
        JobCrud().delete_jobs_by_quote_id(quote_id)
