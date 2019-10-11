from invoicing.crud.client_crud import ClientCrud
from invoicing.crud.company_crud import CompanyCrud
from invoicing.crud.invoice_crud import InvoiceCrud
from invoicing.crud.job_crud import JobCrud
from invoicing.crud.project_crud import ProjectCrud
from invoicing.crud.staff_crud import StaffCrud
from invoicing.crud.status_crud import StatusCrud


class MainController:

    @staticmethod
    def company_action():
        CompanyCrud().menu()

    @staticmethod
    def client_action():
        ClientCrud().menu()

    @staticmethod
    def project_action():
        ProjectCrud().menu()

    @staticmethod
    def invoice_action():
        InvoiceCrud().menu()

    @staticmethod
    def job_action():
        JobCrud().menu()

    @staticmethod
    def staff_action():
        StaffCrud().menu()

    @staticmethod
    def status_action():
        StatusCrud().menu()
