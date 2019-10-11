import os
import re
import subprocess
from pathlib import Path

import jinja2


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

    def create_pdf(self, file_name):
        cmd = 'xelatex -interaction=nonstopmode -halt-on-error "' + file_name + '.tex"'
        return_code = subprocess.call(
            cmd,
            shell=True,
            stdout=open('stdout.txt', 'wb'),
            stderr=open('stderr.txt', 'wb')
        )
        try:
            if not return_code == 0:
                self.remove_generated_pdf_if_exists(file_name)
                raise ValueError('\nError {} executing command: {}'.format(return_code, cmd))
            else:
                self.remove_generation_files(file_name)
                print("\n" + file_name + ".pdf has been generated\n")
        except ValueError as e:
            print("\nError creating pdf: " + str(e))
            print("This is probably an issue with the LaTeX file.\n"
                  "Make sure you have LaTeX installed and try to "
                  "compile the template manually.\n")

    def remove_generation_files(self, file_name):
        # os.unlink(file_name + '.tex')
        os.unlink(file_name + '.aux')
        os.unlink(file_name + '.log')

    def remove_generated_pdf_if_exists(self, file_name):
        output = Path(file_name + '.pdf')
        if output.is_file():
            os.unlink(file_name + '.pdf')

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
