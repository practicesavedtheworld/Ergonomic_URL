class FailedTableCreation(Exception):
    def __init__(self, table_name):
        self.table_name = table_name

    def __str__(self):
        f"""Table {self.table_name} does not exists. Creation failed"""
