from crud.base_crud import BaseCrud
from repository.client_repository import ClientRepository
from repository.quote_repository import QuoteRepository
from ui.menu import Menu
from ui.style import Style


class QuoteCrud(BaseCrud, QuoteRepository):
    def __init__(self):
        super().__init__()
        self.menu('Quote')

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
        quote = self.find_last_reference_code()
        last_reference_code = quote["last_reference_code"] if quote else 'None'
        reference_code = input('Reference Code (Last used: ' + last_reference_code + '): ')
        if client and len(reference_code) > 0:
            self.insert_quote(client['id'], reference_code)
            self.save()
            self.check_rows_updated('Quote Added')
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
                self.remove_quote(quote['id'])
                self.save()
                self.check_rows_updated('Company Deleted')
