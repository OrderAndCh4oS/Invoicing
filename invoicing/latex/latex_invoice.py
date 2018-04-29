from latex.latex_templating import LatexTemplating


class LatexInvoice(LatexTemplating):
    def generate(self, reference_code, company_name, company_address, date, total_cost, jobs):
        template = self.latex_jinja_env.get_template('templates/Invoice.tex')
        if len(jobs) == 0:
            jobs.append({
                'title': '-',
                'description': '-',
                'type': '-',
                'actual_time': '-',
                'staff_rate': '-',
                'cost': '-'
            })
        tex = template.render(
            reference_code=self.tex_escape(reference_code),
            company_name=self.tex_escape(company_name),
            company_address=self.tex_escape(company_address),
            date=self.tex_escape(date),
            total_cost=self.tex_escape(total_cost),
            jobs=[(lambda job: {k: self.tex_escape(v) for k, v in job.items()})(job) for job in jobs]
        )
        file_name = 'invoice'
        self.create_tex_file(tex, file_name)
        self.create_pdf(file_name)


if __name__ == '__main__':
    LatexInvoice().generate(
        'I-7001',
        'Widget Corp',
        '100 Some street, A city, A town, BO41 0PN',
        '14/10/2018',
        '$160',
        [{
            'title': 'Job 1',
            'description': 'Do something',
            'type': 'service',
            'actual_time': '4h',
            'staff_rate': '$40',
            'cost': '$160'
        }]
    )
