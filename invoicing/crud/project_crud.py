import datetime

from actions.action import Action
from crud.base_crud import BaseCrud
from crud.job_crud import JobCrud
from latex.latex_quote import LatexQuote
from repository.client_repository import ClientRepository
from repository.job_repository import JobRepository
from repository.project_repository import ProjectRepository
from ui.date import Date
from ui.menu import Menu
from ui.style import Style


class ProjectCrud(BaseCrud, ProjectRepository):
    def __init__(self):
        super().__init__('Projects')
        super(ProjectRepository, self).__init__('projects')

    def menu(self):
        title = Style.create_title('Manage ' + self.table_name)
        actions = [
            Action('1', 'View', self.show),
            Action('2', 'Add', self.add),
            Action('3', 'Edit', self.edit),
            Action('4', 'Delete', self.delete),
            Action('5', 'Generate', self.generate),
            Action('b', 'Back', False)
        ]
        Menu.create(title, actions)

    def show(self):
        print(Style.create_title('Show Project'))
        project = Menu.select_row(
            self.find_all_join_clients_and_company(),
            self.get_headers(),
            self.find_by_id_join_clients_and_company
        )
        if project:
            print(Style.create_title('Project Data'))
            print('Company: ' + project['company_name'])
            print('Client: ' + project['client_fullname'])
            print('Date: ' + project['date'])
            print('Reference Code: ' + project['reference_code'])
            # Todo: print project items
            Menu.waitForInput()

    def add(self):
        print(Style.create_title('Create Project'))
        clientRepository = ClientRepository()
        client = Menu.select_row(
            clientRepository.find_all(),
            clientRepository.get_headers(),
            clientRepository.find_by_id
        )
        reference_code = self.make_next_reference_code()
        if client and len(reference_code) > 0:
            self.insert({
                'client_id': client['id'],
                'reference_code': reference_code,
                'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            self.save()
            self.check_rows_updated('Project Added')
            self.add_jobs()
            print('Project created')
        else:
            print('Project not created')
        Menu.waitForInput()

    def add_jobs(self):
        while Menu.yes_no_question('Add job'):
            JobCrud().add()

    def edit(self):
        print(Style.create_title('Edit Project'))
        project = Menu.select_row(
            self.find_all_join_clients_and_company(),
            self.get_headers(),
            self.find_by_id_join_clients_and_company
        )
        if project:
            reference_code = self.update_field(project['reference_code'], 'Reference Code')
            self.update(project['id'], {'reference_code': reference_code})
            self.save()
            self.check_rows_updated('Project Updated')
            self.add_jobs()
            Menu.waitForInput()

    def generate(self):
        print(Style.create_title('Generate Quote'))
        project = Menu.select_row(
            self.find_all_join_clients_and_company(),
            self.get_headers(),
            self.find_by_id_join_clients_and_company
        )
        if project:
            jobs = JobRepository().find_jobs_by_project_id(project['id'])
            project_data = {
                'reference_code': project['reference_code'],
                'company_name': project['company_name'],
                'company_address': project['company_address'],
                'date': Date().convert_date_time_for_printing(project['date']),
                'total_cost': '£' + str(sum([float(job['rate']) * float(job['estimated_time']) for job in jobs])),
                'jobs': [{
                    'title': job['title'],
                    'description': job['description'],
                    'type': 'hours',
                    'estimated_time': str(job['estimated_time']),
                    'staff_rate': '£' + str(job['rate']),
                    'cost': '£' + str(float(job['rate']) * float(job['estimated_time']))
                } for job in jobs]
            }
            LatexQuote().generate(**project_data)
            Menu.waitForInput()

    def delete(self):
        print(Style.create_title('Delete Project'))
        project = Menu.select_row(
            self.find_all_join_clients_and_company(),
            self.get_headers(),
            self.find_by_id_join_clients_and_company
        )
        if project:
            user_action = False
            while not user_action == 'delete':
                user_action = input('Type \'delete\' to remove this project or \'c\' to cancel: ')
                if user_action == 'c':
                    return
            if user_action == 'delete':
                self.remove_children(project['id'])
                self.remove(project['id'])
                self.save()
                self.check_rows_updated('Project Deleted')
                Menu.waitForInput()

    def delete_projects_by_client_id(self, client_id):
        projects = self.find_projects_by_client_id(client_id)
        for project in projects:
            self.remove_children(project['id'])
        self.remove_projects_by_client_id(client_id)
        self.save()

    def remove_children(self, project_id):
        JobCrud().delete_jobs_by_project_id(project_id)
