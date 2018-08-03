from flask import Flask

app = Flask(__name__)

from api.company_api import CompanyAPI
from api.client_api import ClientAPI
from api.index_api import IndexAPI
from api.invoice_api import InvoiceAPI
from api.job_api import JobAPI
from api.project_api import ProjectAPI
from api.staff_api import StaffAPI
from api.status_api import StatusAPI


def json_response(json):
    response = app.response_class(
        response=json,
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/')
def index():
    api = IndexAPI()
    return json_response(api.get())


@app.route('/company')
def company_show_all():
    api = CompanyAPI()
    return json_response(api.show_all())


@app.route('/client')
def client_show_all():
    api = ClientAPI()
    return json_response(api.show_all())


@app.route('/staff')
def staff_show_all():
    api = StaffAPI()
    return json_response(api.show_all())


@app.route('/status')
def status_show_all():
    api = StatusAPI()
    return json_response(api.show_all())


@app.route('/project')
def project_show_all():
    api = ProjectAPI()
    return json_response(api.show_all())


@app.route('/job')
def job_show_all():
    api = JobAPI()
    return json_response(api.show_all())


@app.route('/invoice')
def invoice_show_all():
    api = InvoiceAPI()
    return json_response(api.show_all())
