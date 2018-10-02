from setuptools import setup, find_packages

readme = open('README.md', 'r')
README_TEXT = readme.read()
readme.close()


setup(
    name='invoicing',
    version='0.1.3',
    url='',
    license='MIT',
    author='sarcoma',
    author_email='sean@orderandchaoscreative.com',
    description='Generate invoice PDF from LaTeX template',
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'invoicing=invoicing.__main__:main',
        ],
    },
    packages=find_packages(exclude=['*.pdf', 'contrib', 'docs', 'tests*']),
    package_data={
        'invoicing': ['sqlite/invoicing_live.db'],
    },
    python_requires='>=3.5',
    install_requires=['text_template', 'ansi_colours'],
    project_urls={
        'Order & Chaos Creative': 'https://orderandchaoscreative.com',
    },
)
