import json
import uuid
from os import path


class MicroDB:

    def __init__(self, name):
        # Initialize a database with "name"
        self.db = {"schema": {}}
        self.db_name = name
        db_path = path.abspath(f"micro_db/database/{name}.microdb")

        if path.exists(db_path):
            with open(db_path) as f:
                raw = f.readlines()
                nraw = ""
                if len(raw) > 0:
                    for i in raw:
                        nraw += i.replace("\n", "")
                self.db = json.loads(nraw or raw[0])

        self.write_db()

    def write_db(self):
        with open(path.abspath(f"micro_db/database/{self.db_name}.microdb"),
                  "w") as f:
            f.write(json.dumps(self.db))
            f.close()

    def create_table(self, name, schema, unique):
        if self.db.__contains__(name):
            return self.db['schema'][name]

        # Create a new table
        table_schema = {'unique': unique}
        for column in schema:
            table_schema[column] = ""

        self.db["schema"][name] = table_schema
        self.db[name] = []
        self.write_db()

    def add_to_table(self, name, data):
        # In case the item already exists in the table, skip
        unique = self.db["schema"][name]["unique"]
        if self.fetch_one_from_table(name, unique, data[unique]) != None:
            return

        # Add item to the specified table
        schema = self.db["schema"][name]

        new_entry = {'id': str(uuid.uuid4())}
        for column in schema:
            if column == "unique" or column == "id": continue
            new_entry[column] = data[column]

        self.db[name].append(new_entry)
        self.write_db()

    def update_on_table(self, name, ident, delta):
        # Update the row at the identifier with the delta
        unique = self.db["schema"][name]["unique"]
        old = self.fetch_one_from_table(name, unique, ident)

        table = self.db[name]
        delta['id'] = old['id']

        for i, row in enumerate(table):
            if row['id'] == old['id']:
                table[i] = delta

        self.db[name] = table
        self.write_db()

    def delete_on_table(self, name, ident):
        # Get the table and delete the row at the identifier
        for i, row in enumerate(self.db[name]):
            if row[self.db["schema"][name]["unique"]] == ident:
                del self.db[name][i]

        self.write_db()

    def fetch_one_from_table(self, name, column, value):
        # Fetch the first instance of the value appearing in table
        table = self.db[name]

        for row in table:
            if row[column] == value:
                return row
        return None

    def fetch_all_from_table(self, name, column="", value=""):
        # Fetch all instances of the value appearing in table
        if column == "" and value == "": return self.db[name]
        table = self.db[name]
        rows = []

        for row in table:
            if row[column] == value:
                rows.append(row)

        return rows

    def copy(self):
        return self