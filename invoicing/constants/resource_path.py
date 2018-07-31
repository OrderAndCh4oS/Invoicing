import os

import pkg_resources

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../../Invoicing.db")

TEMPLATE_PATH = pkg_resources.resource_filename('invoicing', 'templates/')
