from invoicing.crud.base_crud import BaseCrud
from invoicing.latex.latex_quote import LatexQuote
from invoicing.models.project_model import ProjectModel
from invoicing.repository.job_repository import JobRepository
from invoicing.repository.project_repository import ProjectRepository
from invoicing.ui.date import Date
from invoicing.ui.menu import Menu
from invoicing.ui.style import Style


class ProjectCrud(BaseCrud):
    def __init__(self):
        super().__init__('Projects', ProjectRepository, ProjectModel)
        self.menu_actions.add_action('Generate', self.generate)

    def make_paginated_menu(self):
        return self.paginated_menu(
            find=self.repository.find_paginated_join_company,
            find_by_id=self.repository.find_by_id_join_company
        )

    def generate(self):
        print(Style.create_title('Generate Quote'))
        project = self.paginated_menu(
            find=self.repository.find_paginated_join_company,
            find_by_id=self.repository.find_by_id_join_company
        )
        if project:
            jobs = JobRepository().find_jobs_by_project_id(project['id'])
            project_data = {
                'reference_code': project['reference_code'],
                'company_name': project['company_name'],
                'company_address': project['company_address'],
                'created_at': Date().convert_date_time_for_printing(project['created_at']),
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

