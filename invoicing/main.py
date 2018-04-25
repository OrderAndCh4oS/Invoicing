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
                CompanyCrud().menu('Company')
            elif user_selection == 2:
                ClientCrud().menu('Client')
            elif user_selection == 3:
                QuoteCrud().menu('Quote')
            elif user_selection == 4:
                JobCrud().menu('Job')
            elif user_selection == 5:
                pass
            elif user_selection == 6:
                StaffCrud().menu('Staff')
            elif user_selection == 7:
                StatusCrud().menu('Status')


if __name__ == '__main__':
    Invoicing()
