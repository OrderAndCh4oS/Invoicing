from setuptools import setup

setup(
    name='Invoicing',
    version='0.1.0',
    packages=[],
    url='',
    license='MIT',
    author='sarcoma',
    author_email='sean@orderandchaoscreative.com',
    description='Generate invoice PDF from LaTeX template',
    long_description_content_type = 'text/markdown',
    python_requires='>=3.5',
    install_requires=['text_template', 'ansi_colours'],
    project_urls={
        'Order & Chaos Creative': 'https://orderandchaoscreative.com',
    },
)
