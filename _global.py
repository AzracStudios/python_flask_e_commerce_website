from micro_db import database
import db_init

# DATABASE
db = database.MicroDB("tee_vista")

# INITIALIZE DATABASE WITH TABLES AND VALUES
db_init.init(db)
