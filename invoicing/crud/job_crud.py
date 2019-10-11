from invoicing.actions.action_collection import ActionCollection
from invoicing.crud.base_crud import BaseCrud
from invoicing.models.job_model import JobModel
from invoicing.repository.job_repository import JobRepository
from invoicing.repository.status_repository import StatusRepository
from invoicing.ui.menu import Menu
from invoicing.ui.pagination import Pagination
from invoicing.ui.style import Style
from invoicing.value_validation.value_validation import Validation


class JobCrud(BaseCrud):
    def __init__(self):
        super().__init__('Jobs', JobRepository, JobModel)

    def show_item_menu(self, id):
        Menu.create(self.table_name + ' Menu', ActionCollection(
            ('Update Status', lambda: self.update_status(id)),
            ('Log Time', lambda: self.log_time(id))
        ))

    def make_paginated_menu(self):
        return self.paginated_menu(
            find=self.repository.find_paginated_join_staff_and_status,
            find_by_id=lambda id: self.repository.find_by_id(id, (
                'id', 'reference_code', 'title', 'description',
                'estimated_time', 'actual_time', 'deadline',
                'assigned_to', 'status_id', 'project_id'
            ))
        )

    def log_time(self, job_id):
        logged_time = ''
        while not Validation.is_float(logged_time):
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
