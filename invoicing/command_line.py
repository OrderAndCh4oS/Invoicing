from invoicing.actions.action import Action
from invoicing.actions.action_collection import ActionCollection
from invoicing.controller.main_controller import MainController
from invoicing.ui.menu import Menu


class Invoicing:
    def __init__(self):
        controller = MainController()
        Menu.create('Manage', ActionCollection(
            ('Companies', controller.companyAction),
            ('Clients', controller.clientAction),
            ('Staff', controller.staffAction),
            ('Statuses', controller.statusAction),
            ('Projects', controller.projectAction),
            ('Jobs', controller.jobAction),
            ('Invoices', controller.invoiceAction),
            exit_action=Action('q', 'Quit', False)
        ))


if __name__ == '__main__':
    Invoicing()
