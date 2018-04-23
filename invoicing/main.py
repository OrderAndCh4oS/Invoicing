from company import Company
from client import Client
from ui.menu import Menu

class Invoicing:
    def __init__(self):
        self.main()

    def main(self):
        while True:
            manage = ['Companies', 'Clients', 'Quotes', 'Invoices']
            user_selection = Menu.create('Manage', manage)
            if user_selection == 1:
                Company()
            if user_selection == 2:
                Client()


if __name__ == '__main__':
    Invoicing()
