from actions.action import Action
from crud.base_crud import BaseCrud
from crud.job_crud import JobCrud
from repository.staff_repository import StaffRepository
from ui.menu import Menu
from ui.style import Style


# Todo: show jobs assigned to staff member
# Todo: Log time against staff members jobs
class StaffCrud(BaseCrud, StaffRepository):
    def __init__(self):
        super().__init__('Staff')
        super(StaffRepository, self).__init__('staff')

    def view_staff_menu(self, staff_id):
        print(Style.create_title(self.table_name + 'Menu'))
        actions = [
            Action('1', 'Show Assigned Jobs', lambda: JobCrud().show_jobs_by_assigned_to(staff_id)),
            Action('b', 'Back', False)
        ]
        Menu.create(actions)

    def show(self):
        print(Style.create_title('Show Staff'))
        staff = Menu.select_row(self, 'Staff')
        if staff:
            print(Style.create_title('Staff Data'))
            print('First Name: ' + staff['first_name'])
            print('Last Name: ' + staff['last_name'])
            print('Job Title: ' + staff['job_title'])
            print('Rate: ' + str(staff['rate']))
            self.view_staff_menu(staff['id'])

    def add(self):
        print(Style.create_title('Add Staff'))
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        job_title = input("Job Title: ")
        rate = input("Rate: ")
        if len(first_name) > 0 and len(last_name) and len(job_title) > 0:
            self.insert({'first_name': first_name, 'last_name': last_name, 'job_title': job_title, 'rate': rate})
            self.save()
            self.check_rows_updated('Staff Added')
        else:
            print('Staff not added')

    def edit(self):
        print(Style.create_title('Edit Staff'))
        staff = Menu.select_row(self, 'Staff')
        if staff:
            first_name = self.update_field(staff['first_name'], 'First Name')
            last_name = self.update_field(staff['last_name'], 'Last Name')
            job_title = self.update_field(staff['job_title'], 'Job Title')
            rate = self.update_field(staff['rate'], 'Rate')
            self.update(
                staff['id'],
                {'first_name': first_name, 'last_name': last_name, 'job_title': job_title, 'rate': rate}
            )
            self.save()
            self.check_rows_updated('Staff Updated')
        else:
            print('No changes made')

    def delete(self):
        print(Style.create_title('Delete Staff'))
        staff = Menu.select_row(self, 'Staff')
        if staff:
            user_action = False
            while not user_action == 'delete':
                user_action = input('Type \'delete\' to remove this staff member or \'c\' to cancel: ')
                if user_action == 'c':
                    return
            if user_action == 'delete':
                self.remove(staff['id'])
                self.save()
                self.check_rows_updated('Staff Member Deleted')
