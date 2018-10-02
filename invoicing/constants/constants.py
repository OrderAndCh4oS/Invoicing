from pkg_resources import resource_filename

DB_PATH = resource_filename('invoicing', '/sqlite')
DB = DB_PATH + '/invoicing_live.db'
TEMPLATE_PATH = resource_filename('invoicing', '/templates')
