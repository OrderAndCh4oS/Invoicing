from actions.action import Action
from crud.base_crud import BaseCrud
from crud.job_crud import JobCrud
from models.staff_model import StaffModel
from repository.staff_repository import StaffRepository
from ui.menu import Menu
from ui.style import Style


# Todo: show jobs assigned to staff member
# Todo: Log time against staff members jobs
class StaffCrud(BaseCrud):
    def __init__(self):
        super().__init__('Staff', StaffRepository(), StaffModel())

    def show_item_menu(self, id):
        title = Style.create_title(self.table_name + 'Menu')
        actions = [
            Action('1', 'Show Assigned Jobs', lambda: JobCrud().show_jobs_by_assigned_to(id)),
            Action('b', 'Back', False)
        ]
        Menu.create(title, actions)
