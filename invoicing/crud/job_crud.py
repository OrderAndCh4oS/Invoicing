from _datetime import datetime

from actions.action_collection import ActionCollection
from crud.base_crud import BaseCrud
from models.job_model import JobModel
from repository.job_repository import JobRepository
from repository.project_repository import ProjectRepository
from repository.staff_repository import StaffRepository
from repository.status_repository import StatusRepository
from ui.date import Date
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

    def view_job_menu(self, job_id):
        Menu.create('Job Menu', ActionCollection(
            ('Update Status', lambda: self.update_status(job_id)),
            ('Log Time', lambda: self.log_time(job_id)),
        ))

    def show(self):
        print(Style.create_title('Show Job'))
        job = self.make_pagination_menu()
        if job:
            self.display_job(job)
            self.view_job_menu(job['id'])

    def make_pagination_menu(self):
        return self.paginated_menu(
            find=self.repository.find_paginated_join_staff_and_status,
            find_by_id=lambda id: self.repository.find_by_id(
                id,
                ('id', 'reference_code', 'title', 'description', 'estimated_time', 'actual_time', 'deadline')
            )
        )

    def display_job(self, job):
        print(Style.create_title('Job Data'))
        print('Reference Code: ' + job['reference_code'])
        print('Title: ' + job['title'])
        print('Description: ' + job['description'])
        print('Est. Time: ' + str(job['estimated_time']))
        print('Actual Time: ' + str(job['actual_time']))

    def add(self):
        print(Style.create_title('Add Job'))
        reference_code = self.repository.make_next_reference_code()
        title = input("Title: ")
        description = input("Description: ")
        estimated_time = input("Est. Time: ")
        deadline = input("Deadline (DD-MM-YYYY): ")
        deadline = Date().convert_date_for_saving(deadline)
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        print(Style.create_title('Assign Job To'))
        staff_repository = StaffRepository()
        staff_paginated_menu = Pagination(staff_repository)
        staff_member_assigned = staff_paginated_menu(
            find=staff_repository.find_paginated,
            find_by_id=staff_repository.find_by_id
        )
        print(Style.create_title('Set Status'))
        statusRepository = StatusRepository()
        status_paginated_menu = Pagination(statusRepository)
        status = status_paginated_menu(
            find=statusRepository.find_paginated,
            find_by_id=statusRepository.find_by_id
        )
        last_project = ProjectRepository().find_last_inserted_id()
        if len(title) > 0 and len(estimated_time) > 0 and status:
            self.repository.insert({
                'reference_code': reference_code,
                'title': title,
                'description': description,
                'estimated_time': estimated_time,
                'deadline': deadline,
                'created_at': created_at,
                'status_id': status['id'],
                'assigned_to': staff_member_assigned['id'],
                'project_id': last_project['id']
            })
            self.repository.save()
            self.repository.check_rows_updated('Job Added')
        else:
            print('Job not added')

    def edit(self):
        print(Style.create_title('Edit Job'))
        job = self.make_pagination_menu()
        if job:
            reference_code = self.update_field(job['reference_code'], 'Reference Code')
            title = self.update_field(job['title'], 'Title')
            description = self.update_field(job['description'], 'Description')
            estimated_time = self.update_field(job['estimated_time'], 'Est. Time')
            deadline = self.update_date_field(job['deadline'], 'deadline')
            deadline = Date.convert_date_for_saving(deadline)
            self.repository.update(job['id'], {
                'reference_code': reference_code,
                'title': title,
                'description': description,
                'estimated_time': estimated_time,
                'deadline': deadline
            })
            self.repository.save()
            self.repository.check_rows_updated('Job Updated')
        else:
            print('No changes made')
        Menu.wait_for_input()

    def update_date_field(self, date, title):
        if date != '':
            current_deadline = Date.convert_date_for_printing(date)
        else:
            current_deadline = 'DD-MM-YYYY'
        return self.update_field(current_deadline, title)

    def edit_billable_time(self, job):
        print("Estimated Time: " + job['estimated_time'])
        print("Actual Time: " + job['actual_time'])
        billable_time = input("Billable Time: ")
        self.repository.update_billable_time(job['id'], billable_time)
        self.repository.save()
        self.repository.check_rows_updated('Job Updated')
        Menu.wait_for_input()

    def delete(self):
        print(Style.create_title('Delete Job'))
        job = self.make_pagination_menu()
        if job:
            user_action = False
            while not user_action == 'delete':
                user_action = input('Type \'delete\' to remove this job or \'c\' to cancel: ')
                if user_action == 'c':
                    return
            if user_action == 'delete':
                self.repository.remove(job['id'])
                self.repository.save()
                self.repository.check_rows_updated('Job Deleted')
                Menu.wait_for_input()

    def delete_jobs_by_project_id(self, project_id):
        self.repository.remove_jobs_by_project_id(project_id)
        self.repository.save()

    def delete_jobs_by_invoice_id(self, invoice_id):
        self.repository.remove_jobs_by_invoice_id(invoice_id)
        self.repository.save()

    def show_jobs_by_assigned_to(self, staff_id):
        print(Style.create_title('Select job to log time'))
        job = self.paginated_menu(
            find=lambda: self.repository.find_by_assigned_to(staff_id),
            find_by_id=self.repository.find_by_id
        )
        if job:
            self.display_job(job)
            self.view_job_menu(job['id'])

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
            find=statusRepository.find_all,
            find_by_id=statusRepository.find_by_id
        )
        self.repository.update(job_id, {
            'status_id': status['id'],
        })
        self.repository.save()
        self.repository.check_rows_updated('Status Updated')
        Menu.wait_for_input()
