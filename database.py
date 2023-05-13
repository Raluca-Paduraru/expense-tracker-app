""" A module for the persistence layer """

import sqlite3


class DatabaseManager:
    """ A class specialized for persistence layer using SQLite """

    def __init__(self, database_filename: str):
        """ Initialize the connection with SQLite database """
 
        self.connection = sqlite3.connect(database_filename)
        # created an att cursor that i will use after every command construction
        # that executes it(instead of creating a separate method)
        self.cursor = self.connection.cursor()    

    def __del__(self):
        """ Closes the connection when database manager is no longer used """

        self.connection.close()    

    def create_table(self, table_name: str, columns: dict):
        """ 
        Takes in a table name and the columns with names as keys and types as
        values and creates the CREATE TABLE statement to be executed with SQLite
        """
        columns_with_types = []
        for column_name, data_type in columns.items():
            current_column=f"{column_name} {data_type.upper()}"
            columns_with_types.append(current_column)

        columns_in_statement = ", ".join(columns_with_types)

        statement = f"""
            CREATE TABLE IF NOT EXISTS {table_name}(
                {columns_in_statement}
            );
        """
        self.cursor.execute(statement)
    
    def drop_table(self, table_name: str):
        """ 
        Takes in a table name to delete using the DROP TABLE statement to be
        executed with SQLite
        """
        statement = f"DROP TABLE {table_name};"
        self.cursor.execute(statement)

       