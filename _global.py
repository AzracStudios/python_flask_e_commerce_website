from micro_db import database
from mysql_api import api
import db_init

# DATABASE
db = api.MysqlAPI("tee_vista")
udb = database.MicroDB("tee_vista_users")

# INITIALIZE DATABASE WITH TABLES AND VALUES
db_init.init(db, udb)
