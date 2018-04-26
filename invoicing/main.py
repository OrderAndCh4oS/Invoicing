from actions.action import Action
from controller.main_controller import MainController
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
            controller = MainController()
            actions = [
                Action('1', 'Companies', controller.companyAction),
                Action('2', 'Clients', controller.clientAction),
                Action('3', 'Quotes', controller.quoteAction),
                Action('4', 'Jobs', controller.jobAction),
                Action('5', 'Invoices', controller.invoiceAction),
                Action('6', 'Staff', controller.staffAction),
                Action('7', 'Statuses', controller.statusAction)
            ]
            Menu.create('Manage', actions)

if __name__ == '__main__':
    Invoicing()
