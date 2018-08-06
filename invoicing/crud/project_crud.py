from crud.base_crud import BaseCrud
from crud.job_crud import JobCrud
from latex.latex_quote import LatexQuote
from models.project_model import ProjectModel
from repository.job_repository import JobRepository
from repository.project_repository import ProjectRepository
from ui.date import Date
from ui.menu import Menu
from ui.style import Style


class ProjectCrud(BaseCrud):
    def __init__(self):
        super().__init__('Projects', ProjectRepository, ProjectModel)
        self.repository = ProjectRepository()
        self.menu_actions.add_action('Generate', self.generate)

    # def add(self):
    #     print(Style.create_title('Create Project'))
    #     print(Style.create_title('Select Client'))
    #     clientRepository = ClientRepository()
    #     client = Menu.pagination_menu(
    #         clientRepository,
    #         find=clientRepository.find_paginated_join_companies,
    #         find_by_id=clientRepository.find_by_id_join_company
    #     )
    #     reference_code = self.repository.make_next_reference_code()
    #     if client and len(reference_code) > 0:
    #         self.repository.insert({
    #             'client_id': client['id'],
    #             'reference_code': reference_code,
    #             'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    #         })
    #         self.repository.save()
    #         self.repository.check_rows_updated('Project Added')
    #         self.add_jobs()
    #         print('Project created')
    #     else:
    #         print('Project not created')
    #     Menu.wait_for_input()

    # Todo: one to many relationships
    # Todo: Reference code set by sqlite3 trigger
    # Todo: Date created at can be set with sqlite3

    def add_relations(self):
        self.add_jobs()

    def add_jobs(self):
        while Menu.yes_no_question('Add job'):
            JobCrud().add()

    def edit(self):
        print(Style.create_title('Edit Project'))
        project = self.make_pagination_menu()
        if project:
            reference_code = self.update_field(project['reference_code'], 'Reference Code')
            self.repository.update(project['id'], {'reference_code': reference_code})
            self.repository.save()
            self.repository.check_rows_updated('Project Updated')
            self.add_jobs()
            Menu.wait_for_input()

    def make_pagination_menu(self):
        return self.paginated_menu(
            find=self.repository.find_paginated_join_clients_and_company,
            find_by_id=self.repository.find_by_id_join_clients_and_company
        )

    def generate(self):
        print(Style.create_title('Generate Quote'))
        project = self.make_pagination_menu()
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
            Menu.wait_for_input()

    def delete(self):
        print(Style.create_title('Delete Project'))
        project = self.make_pagination_menu()
        if project:
            user_action = False
            while not user_action == 'delete':
                user_action = input('Type \'delete\' to remove this project or \'c\' to cancel: ')
                if user_action == 'c':
                    return
            if user_action == 'delete':
                self.remove_children(project['id'])
                self.repository.remove(project['id'])
                self.repository.save()
                self.repository.check_rows_updated('Project Deleted')
                Menu.wait_for_input()

    def delete_projects_by_client_id(self, client_id):
        projects = self.repository.find_projects_by_client_id(client_id)
        for project in projects:
            self.remove_children(project['id'])
        self.repository.remove_projects_by_client_id(client_id)
        self.repository.save()

    def remove_children(self, project_id):
        JobCrud().delete_jobs_by_project_id(project_id)
