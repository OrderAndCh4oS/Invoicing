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
            reference_code=self.tex_escape(reference_code),
            company_name=self.tex_escape(company_name),
            company_address=self.tex_escape(company_address),
            date=self.tex_escape(date),
            total_cost=self.tex_escape(total_cost),
            jobs=[(lambda job: {k: self.tex_escape(v) for k, v in job.items()})(job) for job in jobs]
        ))

    def tex_escape(self, text):
        """
            :param text: a plain text message
            :return: the message escaped to appear correctly in LaTeX
        """
        conv = {
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '~': r'\textasciitilde{}',
            '^': r'\^{}',
            '\\': r'\textbackslash{}',
            '<': r'\textless ',
            '>': r'\textgreater ',
        }
        regex = re.compile(
            '|'.join(re.escape(key) for key in sorted(conv.keys(), key=lambda item: - len(item))))
        return regex.sub(lambda match: conv[match.group()], text)

if __name__ == '__main__':
    LatexTemplating().generate_quote(
        'Q-7001',
        'Widget Corp',
        '100 Some street, A city, A town, BO41 0PN',
        '14/10/2018',
        '$160',
        [{
            'title': 'Job 1',
            'description': 'Do something',
            'type': 'time',
            'estimated_time': '4h',
            'staff_rate': '$40',
            'cost': '$160'
        }]
    )
