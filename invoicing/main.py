from actions.action import Action
from controller.main_controller import MainController
from ui.menu import Menu
from ui.style import Style


class Invoicing:
    def __init__(self):
        self.main()

    def main(self):
        print(Style.create_title('Manage'))
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
            Menu.create(actions)

if __name__ == '__main__':
    Invoicing()
