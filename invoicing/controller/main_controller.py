from crud.client_crud import ClientCrud
from crud.company_crud import CompanyCrud
from crud.invoice_crud import InvoiceCrud
from crud.job_crud import JobCrud
from crud.project_crud import ProjectCrud
from crud.staff_crud import StaffCrud
from crud.status_crud import StatusCrud


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
