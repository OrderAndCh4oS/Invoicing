from actions.action import Action
from crud.base_crud import BaseCrud
from crud.job_crud import JobCrud
from repository.client_repository import ClientRepository
from repository.quote_repository import QuoteRepository
from ui.menu import Menu
from ui.style import Style


class QuoteCrud(BaseCrud, QuoteRepository):
    def __init__(self):
        super().__init__('Quotes')
        super(QuoteRepository, self).__init__()

    def menu(self):
        Style.create_title('Manage ' + self.table_name)
        actions = [
            Action('1', 'View', self.show),
            Action('2', 'Add', self.add),
            Action('3', 'Edit', self.edit),
            Action('4', 'Delete', self.delete),
            Action('5', 'Generate', self.generate),
            Action('b', 'Back', False)
        ]
        Menu.create(actions)

    def show(self):
        print(Style.create_title('Show Quote'))
        quote = Menu.select_row(self, 'Quotes')
        if quote:
            print('Company: ' + quote['company_name'])
            print('Client: ' + quote['client_fullname'])
            print('Date: ' + quote['date'])
            print('Reference Code: ' + quote['reference_code'])
            # Todo: print quote items
            input('\nContinue?')

    def add(self):
        print(Style.create_title('Add Quote'))
        client = Menu.select_row(ClientRepository(), 'Select Client')
        last_quote = self.find_last_reference_code()
        last_reference_code = last_quote["last_reference_code"] if last_quote else 'Q-7000'
        reference_code = 'Q-' + str(int(last_reference_code[2:]) + 1)
        if client and len(reference_code) > 0:
            self.insert_quote(client['id'], reference_code)
            self.save()
            self.check_rows_updated('Quote Added')
            while True:
                add_job = input('Add job (Y/n): ')
                if add_job == 'n':
                    break
                elif add_job != 'y' and add_job != 'Y' and add_job != '':
                    continue
                JobCrud().add()
        else:
            print('Quote not added')

    def edit(self):
        print(Style.create_title('Edit Quote'))
        quote = Menu.select_row(self, 'Quotes')
        if quote:
            reference_code = self.update_field(quote['reference_code'], 'Reference Code')
            self.update_quote(quote['id'], reference_code)
            self.save()
            self.check_rows_updated('Quote Updated')

    def generate(self):
        print(Style.create_title('Generate Quote'))
        quote = Menu.select_row(self, 'Quotes')
        if quote:
            pass

    def delete(self):
        print(Style.create_title('Delete Quote'))
        quote = Menu.select_row(self, 'Quotes')
        if quote:
            user_action = False
            while not user_action == 'delete':
                user_action = input('Type \'delete\' to remove this quote or \'c\' to cancel: ')
                if user_action == 'c':
                    return
            if user_action == 'delete':
                self.remove_children(quote['id'])
                self.remove_quote(quote['id'])
                self.save()
                self.check_rows_updated('Company Deleted')

    def delete_quotes_by_client_id(self, client_id):
        quotes = self.find_quotes_by_client_id(client_id)
        for quote in quotes:
            self.remove_children(quote['id'])
        self.remove_quotes_by_client_id(client_id)
        self.save()

    def remove_children(self, quote_id):
        JobCrud().delete_jobs_by_quote_id(quote_id)
