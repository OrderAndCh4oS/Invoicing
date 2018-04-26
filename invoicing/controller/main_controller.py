from crud.client_crud import ClientCrud
from crud.company_crud import CompanyCrud
from crud.job_crud import JobCrud
from crud.quote_crud import QuoteCrud
from crud.staff_crud import StaffCrud
from crud.status_crud import StatusCrud


class MainController:

    def companyAction(self):
        CompanyCrud().menu('Company')

    def clientAction(self):
        ClientCrud().menu('Client')

    def quoteAction(self):
        QuoteCrud().menu('Quote')

    def invoiceAction(self):
        pass

    def jobAction(self):
        JobCrud().menu('Job')

    def staffAction(self):
        StaffCrud().menu('Staff')

    def statusAction(self):
        StatusCrud().menu('Status')
