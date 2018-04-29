from actions.action import Action
from crud.base_crud import BaseCrud
from crud.job_crud import JobCrud
from latex.latex_invoice import LatexInvoice
from repository.client_repository import ClientRepository
from repository.invoice_repository import InvoiceRepository
from repository.job_repository import JobRepository
from ui.menu import Menu
from ui.style import Style


class InvoiceCrud(BaseCrud, InvoiceRepository):
    def __init__(self):
        super().__init__('Invoices')
        super(InvoiceRepository, self).__init__()

    def menu(self):
        Style.create_title('Manage ' + self.table_name)
        actions = [
            Action('1', 'View', self.show),
            Action('2', 'Add', self.add),
            Action('3', 'Edit', self.edit),
            Action('4', 'Delete', self.delete),
            Action('5', 'Generate', self.generate),
            Action('b', 'Back', False)
        ]
        Menu.create(actions)

    def show(self):
        print(Style.create_title('Show Invoice'))
        invoice = Menu.select_row(self, 'Invoices')
        if invoice:
            print('Company: ' + invoice['company_name'])
            print('Client: ' + invoice['client_fullname'])
            print('Date: ' + invoice['date'])
            print('Reference Code: ' + invoice['reference_code'])
            # Todo: print invoice items
            input('\nContinue?')

    def add(self):
        print(Style.create_title('Add Invoice'))
        client = Menu.select_row(ClientRepository(), 'Select Client')
        last_invoice = self.find_last_reference_code()
        last_reference_code = last_invoice["last_reference_code"] if last_invoice else 'Q-7000'
        reference_code = 'I-' + str(int(last_reference_code[2:]) + 1)
        if client and len(reference_code) > 0:
            self.insert_invoice(client['id'], reference_code)
            self.save()
            self.check_rows_updated('Invoice Added')
            last_invoice = self.find_last_reference_code()
            while True:
                add_job = input('Add job (Y/n): ')
                if add_job == 'n':
                    break
                elif add_job != 'y' and add_job != 'Y' and add_job != '':
                    continue
                print(Style.create_title('Select Job'))
                jobRepository = JobRepository()
                job = Menu.select_row_by(
                    lambda: jobRepository.find_jobs_by_client_id_where_complete(client['id']),
                    jobRepository.cursor,
                    jobRepository.find_by_id
                )
                if job:
                    # Todo: Enter billable time for job
                    jobRepository = JobRepository()
                    jobRepository.add_to_invoice(job['id'], last_invoice['id'])
                    jobRepository.save()
            print('\nInvoice added\n')
        else:
            print('Invoice not added')

    def edit(self):
        print(Style.create_title('Edit Invoice'))
        invoice = Menu.select_row(self, 'Invoices')
        if invoice:
            reference_code = self.update_field(invoice['reference_code'], 'Reference Code')
            self.update_invoice(invoice['id'], reference_code)
            self.save()
            self.check_rows_updated('Invoice Updated')

    def generate(self):
        print(Style.create_title('Generate Invoice'))
        invoice = Menu.select_row(self, 'Invoices')
        if invoice:
            jobs = JobRepository().find_jobs_by_invoice_id(invoice['id'])
            invoice_data = {
                'reference_code': invoice['reference_code'],
                'company_name': invoice['company_name'],
                'company_address': invoice['company_address'],
                'date': invoice['date'],
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
            LatexInvoice().generate(**invoice_data)

    def delete(self):
        print(Style.create_title('Delete Invoice'))
        invoice = Menu.select_row(self, 'Invoices')
        if invoice:
            user_action = False
            while not user_action == 'delete':
                user_action = input('Type \'delete\' to remove this invoice or \'c\' to cancel: ')
                if user_action == 'c':
                    return
            if user_action == 'delete':
                self.remove_children(invoice['id'])
                self.remove_invoice(invoice['id'])
                self.save()
                self.check_rows_updated('Invoice Deleted')

    def delete_invoices_by_client_id(self, client_id):
        invoices = self.find_invoices_by_client_id(client_id)
        for invoice in invoices:
            self.remove_children(invoice['id'])
        self.remove_invoices_by_client_id(client_id)
        self.save()

    def remove_children(self, invoice_id):
        JobCrud().delete_jobs_by_invoice_id(invoice_id)
