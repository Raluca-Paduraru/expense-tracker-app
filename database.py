""" A module for the persistence layer """

import sqlite3


class DatabaseManager:
    """ A class specialized for persistence layer using SQLite """

    def __init__(self, database_filename: str):
        """ Initialize the connection with SQLite database """
 
        self.connection = sqlite3.connect(database_filename)
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

    def add(self, table_name: str, data: dict):
        """
        Takes in a table name and INSERT data INTO, and a data dictionary with columns
        as keys and values as values
        """
        column_names = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data.keys()))
        column_values = tuple(data.values())

        statement = f"""
            INSERT INTO
                {table_name} (
                    {column_names}
                ) VALUES (
                    {placeholders}
                );
        """
        self.cursor.execute(statement, column_values)
        self.connection.commit()

    def delete_entry(self, table_name: str, criteria: dict):
        """ 
        Takes in a table name and a criteria to DELETE FROM
        """
        statement = f"DELETE FROM {table_name} WHERE "
        statement += " AND ".join([f"{column} = ?" for column in criteria.keys()])
        values = tuple(criteria.values())
                
        self.cursor.execute(statement, values)
        self.connection.commit()
        
    def select(
            self, table_name:str,  
            criteria:dict=None, 
            order_by=None, 
            descending:bool=False,
            comparison_operator:str=None
            ):
        """
        Takes in a table name and optionally a criteria as a dictionary, a column to order by
        and a boolean flag to order it by that column descending or not
        """

        statement = f"SELECT * FROM {table_name}"
        values = []
        if criteria:
            statement += " WHERE "
            conditions = []
            for column, value in criteria.items():
                if column == "between":
                    conditions.append(f"{value[0]} BETWEEN ? AND ?")
                    values.extend(value[1:])
                elif column == "comparison_operator":
                    conditions.append(f"price {value[0]}?")
                    values.append(value[1])
                else:
                    conditions.append(f"{column} = ?")
                    values.append(value)
            statement += " AND ".join(conditions)
        if order_by:
            statement += f" ORDER BY {order_by}"
            if descending:
                statement += " DESC"
                
        statement += ";"
        
        self.cursor.execute(statement, values)
        return self.cursor.fetchall()
     
    def update(self, table_name:str, data:dict, criteria=None):
        """
         Takes in a table_name, a data dictionary containing the new values for 
         the columns to be updated, and an optional criteria dictionary specifying 
         the conditions for the rows to be updated.
        """
        columns = ', '.join([f"{k} = ?" for k in data.keys()])
        values = list(data.values())
        statement = f"UPDATE {table_name} SET {columns}"
        if criteria:
            statement += " WHERE " + " AND ".join([f"{column} = ?" for column in criteria.keys()])
            values.extend(list(criteria.values()))

        self.cursor.execute(statement, values)
        self.connection.commit()