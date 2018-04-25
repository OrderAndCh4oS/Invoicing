from crud.client_crud import ClientCrud
from crud.company_crud import CompanyCrud
from crud.job_crud import JobCrud
from crud.quote_crud import QuoteCrud
from crud.staff_crud import StaffCrud
from crud.status_crud import StatusCrud
from ui.menu import Menu


class Invoicing:
    def __init__(self):
        self.main()

    def main(self):
        while True:
            manage = ['Companies', 'Clients', 'Quotes', 'Jobs', 'Invoices', 'Staff', 'Statuses']
            user_selection = Menu.create('Manage', manage)
            if user_selection == 1:
                CompanyCrud()
            elif user_selection == 2:
                ClientCrud()
            elif user_selection == 3:
                QuoteCrud()
            elif user_selection == 4:
                JobCrud().menu('Jobs')
            elif user_selection == 5:
                pass
            elif user_selection == 6:
                StaffCrud()
            elif user_selection == 7:
                StatusCrud()


if __name__ == '__main__':
    Invoicing()
