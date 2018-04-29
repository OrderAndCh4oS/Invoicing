from datetime import datetime

from actions.action import Action
from crud.base_crud import BaseCrud
from repository.job_repository import JobRepository
from repository.quote_repository import QuoteRepository
from repository.staff_repository import StaffRepository
from repository.status_repository import StatusRepository
from ui.menu import Menu
from ui.style import Style


class JobCrud(BaseCrud, JobRepository):
    def __init__(self):
        super().__init__('Jobs')
        super(JobRepository, self).__init__()

    def menu(self):
        print(Style.create_title('Manage ' + self.table_name))
        actions = [
            Action('1', 'View', self.show),
            Action('2', 'Edit', self.edit),
            Action('3', 'Delete', self.delete),
            Action('b', 'Back', False)
        ]
        Menu.create(actions)

    def show(self):
        print(Style.create_title('Show Job'))
        job = Menu.select_row(self, 'Jobs')
        if job:
            print(Style.create_title('Job Data'))
            print('Reference Code: ' + job['reference_code'])
            print('Title: ' + job['title'])
            print('Description: ' + job['description'])
            print('Est. Time: ' + job['estimated_time'])
            input('\nContinue?')

    def add(self):
        print(Style.create_title('Add Job'))
        reference_code = self.get_reference_code()
        title = input("Title: ")
        description = input("Description: ")
        estimated_time = input("Est. Time: ")
        deadline = input("Deadline (DD-MM-YYYY): ")
        if len(deadline) > 0:
            deadline = datetime.strptime(deadline, "%d-%m-%Y")
            deadline = deadline.strftime('%Y-%m-%d')
        staff_member_assigned = Menu.select_row(StaffRepository(), 'Assign To')
        status = Menu.select_row(StatusRepository(), 'Set Status')
        last_quote = QuoteRepository().find_last_reference_code()
        if len(title) > 0 and len(estimated_time) > 0 and status:
            self.insert_job(reference_code, title, description, estimated_time, deadline,
                            status['id'], staff_member_assigned['id'], last_quote['id'])
            self.save()
            self.check_rows_updated('Job Added')
        else:
            print('Job not added')

    def edit(self):
        print(Style.create_title('Edit Job'))
        job = Menu.select_row(self, 'Jobs')
        if job:
            reference_code = self.update_field(job['reference_code'], 'Reference Code')
            title = self.update_field(job['title'], 'Title')
            description = self.update_field(job['description'], 'Description')
            estimated_time = self.update_field(job['estimated_time'], 'Est. Time')
            current_deadline = job['deadline'] if job['deadline'] != '' else 'DD-MM-YYYY'
            deadline = self.update_field(current_deadline, 'Deadline')
            self.update_job(job['id'], reference_code, title, description, estimated_time, deadline)
            self.save()
            self.check_rows_updated('Job Updated')
        else:
            print('No changes made')

    def edit_billable_time(self, job):
        print("Estimated Time: " + job['estimated_time'])
        print("Actual Time: " + job['actual_time'])
        billable_time = input("Billable Time: ")
        self.update_billable_time(job['id'], billable_time)
        self.save()
        self.check_rows_updated('Job Updated')

    def edit_actual_time(self, job):
        logged_time = input("Log Time: ")
        self.update_actual_time(job['id'], logged_time)
        self.save()
        self.check_rows_updated('Job Updated')

    def delete(self):
        print(Style.create_title('Delete Job'))
        job = Menu.select_row(self, 'Jobs')
        if job:
            user_action = False
            while not user_action == 'delete':
                user_action = input('Type \'delete\' to remove this job or \'c\' to cancel: ')
                if user_action == 'c':
                    return
            if user_action == 'delete':
                self.remove_job(job['id'])
                self.save()
                self.check_rows_updated('Job Deleted')

    def get_reference_code(self):
        last_job = self.find_last_reference_code()
        last_reference_code = last_job['last_reference_code'] if last_job else 'J-7000'
        reference_code = 'J-' + str(int(last_reference_code[2:]) + 1)
        print(reference_code)
        return reference_code

    def delete_jobs_by_quote_id(self, quote_id):
        self.remove_jobs_by_quote_id(quote_id)
        self.save()

