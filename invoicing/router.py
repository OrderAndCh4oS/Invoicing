from flask import Flask, request

from api.invoice_api import InvoiceAPI
from api.job_api import JobAPI
from api.project_api import ProjectAPI
from api.staff_api import StaffAPI
from api.status_api import StatusAPI

app = Flask(__name__)

from api.company_api import CompanyAPI
from api.client_api import ClientAPI
from api.index_api import IndexAPI


def json_response(json):
    response = app.response_class(
        response=json,
        status=200,
        mimetype='application/json'
    )
    return response


class RequestHandler:
    @staticmethod
    def list(api):
        if request.method == 'POST':
            return json_response(api.add(request.get_json()))
        else:
            return json_response(api.show_all())

    @staticmethod
    def detail(api, id):
        if request.method == 'POST':
            return json_response(api.update_by_id(id, request.get_json()))
        else:
            return json_response(api.show_by_id(id))

@app.route('/')
def index():
    api = IndexAPI()
    return json_response(api.get())


@app.route('/company', methods=['GET', 'POST'])
def company_list():
    return RequestHandler.list(CompanyAPI())


@app.route('/company/<id>', methods=['GET', 'POST'])
def company_detail(id):
    return RequestHandler.detail(CompanyAPI(), id)


@app.route('/client', methods=['GET', 'POST'])
def client_list():
    return RequestHandler.list(ClientAPI())


@app.route('/client/<id>', methods=['GET', 'POST'])
def client_detail(id):
    return RequestHandler.detail(ClientAPI(), id)


@app.route('/staff', methods=['GET', 'POST'])
def staff_list():
    return RequestHandler.list(StaffAPI())


@app.route('/staff/<id>', methods=['GET', 'POST'])
def staff_detail(id):
    return RequestHandler.detail(StaffAPI(), id)


@app.route('/status', methods=['GET', 'POST'])
def status_list():
    return RequestHandler.list(StatusAPI())


@app.route('/status/<id>', methods=['GET', 'POST'])
def status_detail(id):
    return RequestHandler.detail(StatusAPI(), id)


@app.route('/project', methods=['GET', 'POST'])
def project_list():
    return RequestHandler.list(ProjectAPI())


@app.route('/project/<id>', methods=['GET', 'POST'])
def project_detail(id):
    return RequestHandler.detail(ProjectAPI(), id)


@app.route('/job', methods=['GET', 'POST'])
def job_list():
    return RequestHandler.list(JobAPI())


@app.route('/job/<id>', methods=['GET', 'POST'])
def job_detail(id):
    return RequestHandler.detail(JobAPI(), id)


@app.route('/invoice', methods=['GET', 'POST'])
def invoice_list():
    return RequestHandler.list(InvoiceAPI())


@app.route('/invoice/<id>', methods=['GET', 'POST'])
def invoice_detail(id):
    return RequestHandler.detail(InvoiceAPI(), id)
