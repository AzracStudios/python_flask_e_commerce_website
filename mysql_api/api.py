import mysql.connector
import uuid

class MysqlAPI:

    def __init__(self, name):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="azrac",
            password="123",
            database=name
        )
        self.cur = self.mydb.cursor()
        self.schema_buffer = {}

    def create_table(self, name, schema, unique):
        self.schema_buffer[name] = schema
        try:
            cmd = f"create table {name} ("
            for _, n in enumerate(schema):
                cmd += f"{n} varchar(1000){' unique'if n == unique else ''}{', ' if _ < len(schema) - 1 else ''}"
            cmd += ");"
            self.cur.execute(cmd)
        except:
            print(f"table {name} already exists. skipping....")

    def add_to_table(self, name, data):
        try:
            cmd = f"insert into {name} (id, "
            for _, i in enumerate(data.keys()):
                cmd += f"{i}{',' if _ < len(data.keys()) - 1  else ''}"
            cmd += f") values ('{str(uuid.uuid4())}', "
            for _, i in enumerate(data.values()):
                cmd += f"'{i}'{',' if _ < len(data.values()) - 1  else ''}"
            cmd += ")"
            self.cur.execute(cmd)
            self.mydb.commit()
        except:
            print(f"item {data} already exists. skipping...")


    def update_on_table(self, name, delta):
        cmd = f"update {name} set "
        i = 0
        for key, value in delta.items():
            cmd += f"{',' if i != 0 else ''} {key} = '{value}'"
            i+=1
        cmd += f" where id = '{delta['id']}'"
        
        self.cur.execute(cmd)
        self.mydb.commit()

    def delete_on_table(self, name, unique, ident):
        self.cur.execute(f"delete from {name} where {unique} = '{ident}'")
        self.mydb.commit()

    def fetch_one_from_table(self, name, column, value):
        cmd = f"select * from {name} where {column} = '{value}'"
        self.cur.execute(cmd)
        mysql_res = self.cur.fetchone()
        if not mysql_res:
            return
        to_ret = {}
        for _, i in enumerate(self.schema_buffer[name]):
            to_ret[i] = mysql_res[_]

        return to_ret


    def fetch_all_from_table(self, name, column="", value=""):
        cmd = f"select * from {name}"
        if column != "" and value != "":
            cmd += f" where {column} = '{value}'"

        self.cur.execute(cmd)
        mysql_res = self.cur.fetchall()
        to_ret = []

        for ind, res in enumerate(mysql_res):
            to_ret.append({})
            for _, i in enumerate(self.schema_buffer[name]):
                to_ret[ind][i] = res[_]

        return to_ret
        