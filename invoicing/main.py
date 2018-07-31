from actions.action import Action
from controller.main_controller import MainController
from ui.menu import Menu
from ui.style import Style


class Invoicing:
    def __init__(self):
        self.main()

    def main(self):
        title = Style.create_title('Manage')
        controller = MainController()
        actions = [
            # Action('s', 'Show Assigned Jobs', controller.show_assigned_jobs),
            Action('1', 'Companies', controller.companyAction),
            Action('2', 'Clients', controller.clientAction),
            Action('3', 'Staff', controller.staffAction),
            Action('4', 'Statuses', controller.statusAction),
            Action('5', 'Projects', controller.projectAction),
            Action('6', 'Jobs', controller.jobAction),
            Action('7', 'Invoices', controller.invoiceAction),
            Action('q', 'Quit', False)
        ]
        Menu.create(title, actions)

if __name__ == '__main__':
    Invoicing()
