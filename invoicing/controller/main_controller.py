from invoicing.crud.client_crud import ClientCrud
from invoicing.crud.company_crud import CompanyCrud
from invoicing.crud.invoice_crud import InvoiceCrud
from invoicing.crud.job_crud import JobCrud
from invoicing.crud.project_crud import ProjectCrud
from invoicing.crud.staff_crud import StaffCrud
from invoicing.crud.status_crud import StatusCrud


class MainController:

    def companyAction(self):
        CompanyCrud().menu()

    def clientAction(self):
        ClientCrud().menu()

    def projectAction(self):
        ProjectCrud().menu()

    def invoiceAction(self):
        InvoiceCrud().menu()

    def jobAction(self):
        JobCrud().menu()

    def staffAction(self):
        StaffCrud().menu()

    def statusAction(self):
        StatusCrud().menu()
