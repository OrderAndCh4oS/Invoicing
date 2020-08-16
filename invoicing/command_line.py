#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from invoicing.actions.action import Action
from invoicing.actions.action_collection import ActionCollection
from invoicing.controller.main_controller import MainController
from invoicing.ui.menu import Menu


class Invoicing:
    def __init__(self):
        controller = MainController()
        Menu.create('Manage', ActionCollection(
            ('Companies', controller.company_action),
            ('Clients', controller.client_action),
            ('Staff', controller.staff_action),
            ('Statuses', controller.status_action),
            ('Projects', controller.project_action),
            ('Jobs', controller.job_action),
            ('Invoices', controller.invoice_action),
            exit_action=Action('q', 'Quit', False)
        ))


if __name__ == '__main__':
    Invoicing()
