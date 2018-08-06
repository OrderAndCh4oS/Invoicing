from actions.action import Action
from actions.action_collection import ActionCollection
from controller.main_controller import MainController
from ui.menu import Menu
from ui.style import Style


class Invoicing:
    def __init__(self):
        self.main()

    def main(self):
        title = Style.create_title('Manage')
        controller = MainController()
        menu = ActionCollection(
            ('Companies', controller.companyAction),
            ('Clients', controller.clientAction),
            ('Staff', controller.staffAction),
            ('Statuses', controller.statusAction),
            ('Projects', controller.projectAction),
            ('Jobs', controller.jobAction),
            ('Invoices', controller.invoiceAction),
            exit_action=Action('q', 'Quit', False)
        )
        Menu.create(title, menu.actions)


if __name__ == '__main__':
    Invoicing()
