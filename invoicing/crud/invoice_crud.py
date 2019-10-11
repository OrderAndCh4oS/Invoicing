from invoicing.crud.base_crud import BaseCrud
from invoicing.latex.latex_invoice import LatexInvoice
from invoicing.models.invoice_model import InvoiceModel
from invoicing.repository.invoice_repository import InvoiceRepository
from invoicing.repository.job_repository import JobRepository
from invoicing.ui.date import Date
from invoicing.ui.menu import Menu
from invoicing.ui.style import Style
from invoicing.value_validation.value_validation import Validation


class InvoiceCrud(BaseCrud):
    def __init__(self):
        super().__init__('Invoices', InvoiceRepository, InvoiceModel)
        self.menu_actions.add_action('Generate', self.generate)

    def make_paginated_menu(self):
        return self.paginated_menu(
            find=self.repository.find_paginated_join_clients_and_companies,
            find_by_id=self.repository.find_by_id_join_clients_and_companies
        )

    def generate(self):
        print(Style.create_title('Generate Invoice'))
        invoice = self.make_paginated_menu()
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
            while not Validation.is_float(billable):
                billable = input('Billable Time: ')
            jobRepository.update_billable_time(job['id'], billable)
            jobRepository.save()
            jobRepository.check_rows_updated('Job Updated')

    def make_invoice_dictionary(self, invoice, jobs):
        invoice_data = {
            'reference_code': invoice['reference_code'],
            'company_name': invoice['company_name'],
            'company_address': invoice['company_address'],
            'created_at': Date().convert_date_time_for_printing(invoice['created_at']),
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

