from datetime import datetime

from actions.action import Action
from crud.base_crud import BaseCrud
from crud.job_crud import JobCrud
from latex.latex_invoice import LatexInvoice
from repository.client_repository import ClientRepository
from repository.invoice_repository import InvoiceRepository
from repository.job_repository import JobRepository
from ui.date import Date
from ui.menu import Menu
from ui.style import Style
from value_validation.value_validation import Validation


class InvoiceCrud(BaseCrud):
    def __init__(self):
        super().__init__('Invoices')
        self.repository = InvoiceRepository()

    def menu(self):
        title = Style.create_title('Manage ' + self.table_name)
        actions = [
            Action('1', 'View', self.show),
            Action('2', 'Add', self.add),
            Action('3', 'Edit', self.edit),
            Action('4', 'Delete', self.delete),
            Action('5', 'Generate', self.generate),
            Action('b', 'Back', False)
        ]
        Menu.create(title, actions)

    def make_pagination_menu(self):
        return Menu.pagination_menu(
            self.repository,
            find=self.repository.find_paginated_join_clients_and_companies,
            find_by_id=self.repository.find_by_id_join_clients_and_companies
        )

    def add(self):
        print(Style.create_title('Add Invoice'))
        clientRepository = ClientRepository()
        client = Menu.pagination_menu(
            clientRepository,
            find=clientRepository.find_paginated,
            find_by_id=clientRepository.find_by_id
        )
        reference_code = self.generate_reference_code()
        if client and len(reference_code) > 0:
            self.repository.insert({
                'client_id': client['id'],
                'reference_code': reference_code,
                'date': datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            self.repository.save()
            self.repository.check_rows_updated('Invoice Added')
            self.add_client_jobs_to_invoice(client['id'])
            print('\nInvoice added\n')
        else:
            print('\nInvoice not added\n')
        Menu.wait_for_input()

    def generate_reference_code(self):
        last_invoice = self.repository.find_last_reference_code()
        last_reference_code = last_invoice["last_reference_code"] if last_invoice else 'Q-7000'
        reference_code = 'I-' + str(int(last_reference_code[2:]) + 1)
        return reference_code

    def add_client_jobs_to_invoice(self, client_id):
        last_invoice = self.repository.find_last_reference_code()
        while True:
            add_job = Menu.yes_no_question('Add job to invoice')
            if not add_job:
                break
            self.select_job(last_invoice, client_id)

    def select_job(self, last_invoice, client_id):
        print(Style.create_title('Select Job'))
        jobRepository = JobRepository()
        job = Menu.pagination_menu(
            jobRepository,
            find=lambda limit, page: jobRepository.find_paginated_jobs_by_client_id_where_not_complete(client_id, limit,
                                                                                                       page),
            find_by_id=jobRepository.find_by_id
        )
        if job:
            # Todo: Enter billable time for job
            jobRepository.add_to_invoice(job['id'], last_invoice['id'])
            jobRepository.save()
            self.repository.check_rows_updated('Job Added')

    def edit(self):
        print(Style.create_title('Edit Invoice'))
        invoice = self.make_pagination_menu()
        if invoice:
            reference_code = self.update_field(invoice['reference_code'], 'Reference Code')
            self.repository.update(invoice['id'], {'reference_code': reference_code})
            self.repository.save()
            self.repository.check_rows_updated('Invoice Updated')

    def generate(self):
        print(Style.create_title('Generate Invoice'))
        invoice = self.make_pagination_menu()
        if invoice:
            jobRepository = JobRepository()
            jobs = jobRepository.find_jobs_by_invoice_id(invoice['id'])
            self.enter_billable_time(jobRepository, jobs)
            jobs = jobRepository.find_jobs_by_invoice_id(invoice['id'])
            invoice_data = self.make_invoice_dictionary(invoice, jobs)
            LatexInvoice().generate(**invoice_data)
            self.mark_invoiced_jobs_as_complete(jobRepository, jobs)
            Menu.wait_for_input()

    def enter_billable_time(self, jobRepository, jobs):
        print(Style.create_title('Enter Billable Time'))
        for job in jobs:
            print('Title: %s' % job['title'])
            print('Description: %s' % job['description'])
            print('Estimated Time: %s' % job['estimated_time'])
            print('Logged Time: %s' % job['actual_time'])
            billable = ''
            while not Validation.isFloat(billable):
                billable = input('Billable Time: ')
            jobRepository.update_billable_time(job['id'], billable)
            jobRepository.save()
            jobRepository.check_rows_updated('Job Updated')

    def make_invoice_dictionary(self, invoice, jobs):
        invoice_data = {
            'reference_code': invoice['reference_code'],
            'company_name': invoice['company_name'],
            'company_address': invoice['company_address'],
            'date': Date().convert_date_time_for_printing(invoice['date']),
            'total_cost': str(sum([float(job['rate']) * float(job['billable_time']) for job in jobs])),
            'jobs': [{
                'title': job['title'],
                'description': job['description'],
                'type': 'hours',
                'billable_time': str(job['billable_time']),
                'staff_rate': str(job['rate']),
                'cost': str(float(job['rate']) * float(job['billable_time']))
            } for job in jobs]
        }
        return invoice_data

    def mark_invoiced_jobs_as_complete(self, jobRepository, jobs):
        if len(jobs):
            for job in jobs:
                jobRepository.update_mark_as_complete(job['id'])
            jobRepository.save()
            jobRepository.check_rows_updated('The selected jobs have been marked as completed')

    def delete(self):
        print(Style.create_title('Delete Invoice'))
        invoice = self.make_pagination_menu()
        if invoice:
            user_action = False
            while not user_action == 'delete':
                user_action = input('Type \'delete\' to remove this invoice or \'c\' to cancel: ')
                if user_action == 'c':
                    return
            if user_action == 'delete':
                self.remove_children(invoice['id'])
                self.repository.remove(invoice['id'])
                self.repository.save()
                self.repository.check_rows_updated('Invoice Deleted')
                Menu.wait_for_input()

    def delete_invoices_by_client_id(self, client_id):
        invoices = self.repository.find_invoices_by_client_id(client_id)
        for invoice in invoices:
            self.remove_children(invoice['id'])
        self.repository.remove_invoices_by_client_id(client_id)
        self.repository.save()

    def remove_children(self, invoice_id):
        JobCrud().delete_jobs_by_invoice_id(invoice_id)
