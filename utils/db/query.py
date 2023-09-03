class QueryBuilder:
    def __init__(self, table_name, fields_enum, duplicate_fields_enum=None):
        self.table_name = table_name
        self.fields_enum = fields_enum
        self.duplicate_fields_enum = duplicate_fields_enum

    def read_all_query(self):
        return f"SELECT * FROM {self.table_name}"

    def build_insert_query(self, keys):
        field_list = ", ".join(keys)
        placeholders = ", ".join([f"%({field})s" for field in keys])
        return f"INSERT INTO {self.table_name} ({field_list}) VALUES ({placeholders})"

    def build_insert_on_duplicate_key_update_query(self, keys):
        on_duplicate_fields = [field.value for field in self.duplicate_fields_enum]
        update_clause = ", ".join([f"{field} = VALUES({field})" for field in on_duplicate_fields])
        return f"{self.build_insert_query(keys)} ON DUPLICATE KEY UPDATE {update_clause}"
