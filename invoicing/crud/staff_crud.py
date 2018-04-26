from crud.base_crud import BaseCrud
from repository.staff_repository import StaffRepository
from ui.menu import Menu
from ui.style import Style


class StaffCrud(BaseCrud, StaffRepository):
    def __init__(self):
        super().__init__('Staff')
        super(StaffRepository, self).__init__()

    def show(self):
        print(Style.create_title('Show Staff'))
        staff = Menu.select_row(self, 'Staff')
        if staff:
            print(Style.create_title('Staff Data'))
            print('First Name: ' + staff['first_name'])
            print('Last Name: ' + staff['last_name'])
            print('Job Title: ' + staff['job_title'])
            print('Rate: ' + staff['rate'])
            input('\nContinue?')

    def add(self):
        print(Style.create_title('Add Staff'))
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        job_title = input("Job Title: ")
        rate = input("Rate: ")
        if len(first_name) > 0 and len(last_name) and len(job_title) > 0:
            self.insert_staff(first_name, last_name, job_title, rate)
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
            self.update_staff(staff['id'], first_name, last_name, job_title, rate)
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
                self.remove_staff(staff['id'])
                self.save()
                self.check_rows_updated('Staff Member Deleted')
