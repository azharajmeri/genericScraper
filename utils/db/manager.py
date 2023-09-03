from utils.db.connector import MySQLConnector
from utils.db.query import QueryBuilder
from utils.db.settings import DB_CONFIG


class QueryManager:
    def __init__(self, table_name, fields_enum, duplicate_fields_enum=None):
        self.db_config = DB_CONFIG
        self.table_name = table_name
        self.fields_enum = fields_enum
        self.query_builder = QueryBuilder(self.table_name, self.fields_enum, duplicate_fields_enum)

    def _connect_to_db(self):
        return MySQLConnector(**self.db_config)

    def validate_data(self, data):
        expected_fields = {field.value for field in self.fields_enum}
        provided_fields = set(data.keys())

        if missing_fields := expected_fields - provided_fields:
            raise ValueError(f"Missing fields in data: {missing_fields}")

    def read_all(self):
        query = self.query_builder.read_all_query()
        with self._connect_to_db() as conn:
            cursor = conn.cursor(dictionary=True)  # Return results as dictionaries
            cursor.execute(query)
            result = cursor.fetchall()
        return result

    def insert(self, data):
        # Validate data against the enum
        self.validate_data(data)
        query, params = self.query_builder.build_insert_query(data)
        with self._connect_to_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

    def insert_on_duplicate_key_update(self, data):
        # Validate data against the enum
        self.validate_data(data)
        query = self.query_builder.build_insert_on_duplicate_key_update_query(data)
        print(query)
        with self._connect_to_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query, data)
            conn.commit()
