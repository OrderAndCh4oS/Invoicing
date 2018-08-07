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
        self.menu_actions.add_action('Generate', self.generate)

    def add_relations(self):
        while Menu.yes_no_question('Add job'):
            JobCrud().add()

    def generate(self):
        print(Style.create_title('Generate Quote'))
        project = self.paginated_menu(
            find=self.repository.find_paginated_join_clients_and_company,
            find_by_id=self.repository.find_by_id_join_clients_and_company
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
            Menu.wait_for_input()

    def delete_projects_by_client_id(self, client_id):
        projects = self.repository.find_projects_by_client_id(client_id)
        for project in projects:
            self.remove_relations(project['id'])
        self.repository.remove_projects_by_client_id(client_id)
        self.repository.save()

    def remove_relations(self, project_id):
        JobCrud().delete_jobs_by_project_id(project_id)
