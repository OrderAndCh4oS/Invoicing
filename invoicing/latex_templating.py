import os
import re

import jinja2

"""
Max char width for: 
    address col = 28
    ref code and date col = 12 
    client ref col = 18
"""


class LatexTemplating:
    def __init__(self):
        self.latex_jinja_env = jinja2.Environment(
            block_start_string='\BLOCK{',
            block_end_string='}',
            variable_start_string='\VAR{',
            variable_end_string='}',
            comment_start_string='\#{',
            comment_end_string='}',
            line_statement_prefix='%%',
            line_comment_prefix='%#',
            trim_blocks=True,
            autoescape=False,
            loader=jinja2.FileSystemLoader(os.path.abspath('.'))
        )

    def generate_quote(self, reference_code, company_name, company_address, date, total_cost, jobs):
        template = self.latex_jinja_env.get_template('templates/Quote.tex')
        print(template.render(
            reference_code=reference_code,
            company_name=company_name,
            company_address=company_address,
            date=date,
            total_cost=re.escape(total_cost),
            jobs=jobs
        ))


if __name__ == '__main__':
    LatexTemplating().generate_quote(
        'Q-7001',
        'Widget Corp',
        '100 Some street,\\\\\nA city,\\\\\nA town,\\\\\nBO41 0PN',
        '14/10/2018',
        '$160',
        [{
            'title': re.escape('Job 1'),
            'description': re.escape('Do something'),
            'type': re.escape('time'),
            'estimated_time': re.escape('4h'),
            'staff_rate': re.escape('$40'),
            'cost': re.escape('$160')
        }]
    )
