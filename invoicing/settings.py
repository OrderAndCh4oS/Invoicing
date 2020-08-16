from dotenv import load_dotenv
import os
import invoicing.constants.constants as c

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

DB = os.path.join(c.DB_PATH,os.environ.get("DB_FILE"))
