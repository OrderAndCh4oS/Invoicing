from crud.client_crud import ClientCrud
from crud.company_crud import CompanyCrud
from crud.quote_crud import QuoteCrud
from ui.menu import Menu


class Invoicing:
    def __init__(self):
        self.main()

    def main(self):
        while True:
            manage = ['Companies', 'Clients', 'Quotes', 'Invoices']
            user_selection = Menu.create('Manage', manage)
            if user_selection == 1:
                CompanyCrud()
            if user_selection == 2:
                ClientCrud()
            if user_selection == 3:
                QuoteCrud()


if __name__ == '__main__':
    Invoicing()
