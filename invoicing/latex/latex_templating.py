import os
import re
import subprocess

import jinja2


class LatexTemplating:
    """
    Max char width for:
        address col = 28
        ref code and date col = 12
        client ref col = 18
    """

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

    def create_pdf(self, file_name):
        cmd = 'xelatex ' + file_name + '.tex'
        return_code = subprocess.call(cmd, shell=True)
        if not return_code == 0:
            os.unlink(file_name + '.pdf')
            raise ValueError('Error {} executing command: {}'.format(return_code, cmd))
        os.unlink(file_name + '.tex')
        os.unlink(file_name + '.aux')
        os.unlink(file_name + '.log')

    def create_tex_file(self, tex, file_name):
        file = open(file_name + ".tex", "w")
        file.write(tex)
        file.close()

    def tex_escape(self, text):
        """
            :param text: a plain text message
            :return: the message escaped to appear correctly in LaTeX
        """
        conversions = {
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
            '|'.join(re.escape(key) for key in sorted(conversions.keys(), key=lambda item: - len(item))))
        return regex.sub(lambda match: conversions[match.group()], text)
