from actions.action_collection import ActionCollection
from crud.base_crud import BaseCrud
from model_validation.field import ForeignKeyField
from models.job_model import JobModel
from repository.job_repository import JobRepository
from repository.project_repository import ProjectRepository
from repository.status_repository import StatusRepository
from ui.menu import Menu
from ui.pagination import Pagination
from ui.style import Style
from value_validation.value_validation import Validation


class JobCrud(BaseCrud):
    def __init__(self):
        super().__init__('Jobs', JobRepository, JobModel)

    def menu(self):
        Menu.create('Manage ' + self.table_name, ActionCollection(
            ('View', self.show),
            ('Edit', self.edit),
            ('Delete', self.delete),
        ))

    def show_item_menu(self, id):
        Menu.create(self.table_name + ' Menu', ActionCollection(
            ('Update Status', lambda: self.update_status(id)),
            ('Log Time', lambda: self.log_time(id))
        ))

    def make_paginated_menu(self):
        return self.paginated_menu(
            find=self.repository.find_paginated_join_staff_and_status,
            find_by_id=lambda id: self.repository.find_by_id(
                id,
                ('id', 'reference_code', 'title', 'description', 'estimated_time', 'actual_time', 'deadline',
                 'assigned_to', 'status_id')
            )
        )

    def add(self):
        print(Style.create_title('Add %s' % self.table_name))
        data = {}
        for (key, field) in self.model:
            if field.initial_value is not None:
                data[key] = field.initial_value
            elif isinstance(field, ForeignKeyField):
                data[key] = self.select_foreign_key_relationship(field.relationship)
            else:
                data[key] = input("%s: " % self.make_label(key))
        data['project_id'] = ProjectRepository().find_last_inserted_id()['id']
        self.model(**data)
        self.model.validate()
        if self.model.is_valid():
            self.repository.insert(data)
            self.repository.save()
            self.repository.check_rows_updated('%s Added' % self.table_name)
            self.add_relations()
        else:
            print(Style.create_title('%s not added' % self.table_name))
            for (key, value) in self.model.get_errors().items():
                print("%s: %s" % (key.capitalize(), value))
        Menu.wait_for_input()

    def log_time(self, job_id):
        logged_time = ''
        while not Validation.isFloat(logged_time):
            logged_time = input('Log Time: ')
        self.repository.update_actual_time(job_id, logged_time)
        self.repository.save()
        self.repository.check_rows_updated('Job Updated')
        Menu.wait_for_input()

    def update_status(self, job_id):
        statusRepository = StatusRepository()
        paginated_menu = Pagination(statusRepository)
        status = paginated_menu(
            find=statusRepository.find_paginated,
            find_by_id=statusRepository.find_by_id
        )
        self.repository.update(job_id, {
            'status_id': status['id'],
        })
        self.repository.save()
        self.repository.check_rows_updated('Status Updated')
        Menu.wait_for_input()

    def edit_billable_time(self, job):
        print("Estimated Time: " + job['estimated_time'])
        print("Actual Time: " + job['actual_time'])
        billable_time = input("Billable Time: ")
        self.repository.update_billable_time(job['id'], billable_time)
        self.repository.save()
        self.repository.check_rows_updated('Job Updated')
        Menu.wait_for_input()

    def show_jobs_by_assigned_to(self, staff_id):
        print(Style.create_title('Select job to log time'))
        job = self.paginated_menu(
            find=lambda limit, page: self.repository.find_paginated_by_assigned_to(staff_id, limit, page),
            find_by_id=self.repository.find_by_id
        )
        if job:
            self.show_item_detail(job)
            self.show_item_menu(job['id'])

    def delete_jobs_by_project_id(self, project_id):
        self.repository.remove_jobs_by_project_id(project_id)
        self.repository.save()

    def delete_jobs_by_invoice_id(self, invoice_id):
        self.repository.remove_jobs_by_invoice_id(invoice_id)
        self.repository.save()
