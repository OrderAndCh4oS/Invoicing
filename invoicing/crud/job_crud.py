from _datetime import datetime

from actions.action import Action
from crud.base_crud import BaseCrud
from repository.job_repository import JobRepository
from repository.quote_repository import QuoteRepository
from repository.staff_repository import StaffRepository
from repository.status_repository import StatusRepository
from ui.date import Date
from ui.menu import Menu
from ui.style import Style
from validation.validation import Validation


class JobCrud(BaseCrud, JobRepository):
    def __init__(self):
        super().__init__('Jobs')
        super(JobRepository, self).__init__('jobs')

    def menu(self):
        print(Style.create_title('Manage ' + self.table_name))
        actions = [
            Action('1', 'View', self.show),
            Action('2', 'Edit', self.edit),
            Action('3', 'Delete', self.delete),
            Action('b', 'Back', False)
        ]
        Menu.create(actions)

    def view_job_menu(self, job_id):
        print(Style.create_title('Job Menu'))
        actions = [
            Action('1', 'Log Time', lambda: self.log_time(job_id)),
            Action('2', 'Mark as Complete', lambda: self.mark_as_complete(job_id)),
            Action('b', 'Back', False)
        ]
        Menu.create(actions)

    def show(self):
        print(Style.create_title('Show Job'))
        job = Menu.select_row_by(
            self.find_all_join_staff_and_status,
            self.cursor,
            lambda id: self.find_by_id(
                id,
                ('id', 'reference_code', 'title', 'description', 'estimated_time', 'actual_time', 'deadline')
            )
        )
        if job:
            self.display_job(job)
            self.view_job_menu(job['id'])

    def display_job(self, job):
        print(Style.create_title('Job Data'))
        print('Reference Code: ' + job['reference_code'])
        print('Title: ' + job['title'])
        print('Description: ' + job['description'])
        print('Est. Time: ' + str(job['estimated_time']))
        print('Actual Time: ' + str(job['actual_time']))

    def add(self):
        print(Style.create_title('Add Job'))
        reference_code = self.get_reference_code()
        title = input("Title: ")
        description = input("Description: ")
        estimated_time = input("Est. Time: ")
        deadline = input("Deadline (DD-MM-YYYY): ")
        deadline = Date().convert_date_for_saving(deadline)
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        staff_member_assigned = Menu.select_row(StaffRepository(), 'Assign To')
        status = Menu.select_row(StatusRepository(), 'Set Status')
        last_quote = QuoteRepository().find_last_reference_code()
        if len(title) > 0 and len(estimated_time) > 0 and status:
            self.insert({
                'reference_code': reference_code,
                'title': title,
                'description': description,
                'estimated_time': estimated_time,
                'deadline': deadline,
                'created_at': created_at,
                'status_id': status['id'],
                'assigned_to': staff_member_assigned['id'],
                'quote_id': last_quote['id']
            })
            self.save()
            self.check_rows_updated('Job Added')
        else:
            print('Job not added')

    def edit(self):
        print(Style.create_title('Edit Job'))
        job = Menu.select_row_by(
            self.find_all_join_staff_and_status,
            self.cursor,
            lambda id: self.find_by_id(
                id,
                ('id', 'reference_code', 'title', 'description', 'estimated_time', 'actual_time', 'deadline')
            )
        )
        if job:
            reference_code = self.update_field(job['reference_code'], 'Reference Code')
            title = self.update_field(job['title'], 'Title')
            description = self.update_field(job['description'], 'Description')
            estimated_time = self.update_field(job['estimated_time'], 'Est. Time')
            deadline = self.update_date_field(job['deadline'], 'deadline')
            deadline = Date.convert_date_for_saving(deadline)
            self.update(job['id'], {
                'reference_code': reference_code,
                'title': title,
                'description': description,
                'estimated_time': estimated_time,
                'deadline': deadline
            })
            self.save()
            self.check_rows_updated('Job Updated')
        else:
            print('No changes made')

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
        self.update_billable_time(job['id'], billable_time)
        self.save()
        self.check_rows_updated('Job Updated')

    def delete(self):
        print(Style.create_title('Delete Job'))
        job = Menu.select_row_by(
            self.find_all_join_staff_and_status,
            self.cursor,
            lambda id: self.find_by_id(
                id,
                ('id', 'reference_code', 'title', 'description', 'estimated_time', 'actual_time', 'deadline')
            )
        )
        if job:
            user_action = False
            while not user_action == 'delete':
                user_action = input('Type \'delete\' to remove this job or \'c\' to cancel: ')
                if user_action == 'c':
                    return
            if user_action == 'delete':
                self.remove(job['id'])
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

    def delete_jobs_by_invoice_id(self, invoice_id):
        self.remove_jobs_by_invoice_id(invoice_id)
        self.save()

    def show_jobs_by_assigned_to(self, staff_id):
        print(Style.create_title('Select job to log time'))
        job = Menu().select_row_by(
            lambda: self.find_by_assigned_to(staff_id),
            self.cursor,
            self.find_by_id
        )
        if job:
            self.log_time(job['id'])

    def log_time(self, job_id):
        logged_time = False
        while not Validation.isFloat(logged_time):
            logged_time = input('Log Time: ')
        self.update_actual_time(job_id, logged_time)
        self.save()
        self.check_rows_updated('Job Updated')

    def mark_as_complete(self, job_id):
        if Menu.yes_no_question("Would you like to mark this job as complete?"):
            self.update_mark_as_complete(job_id)
            self.save()
            self.check_rows_updated('Job Updated')
