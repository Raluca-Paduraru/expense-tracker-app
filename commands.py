""" A module for the business layer """

import sys
from database import DatabaseManager
from pathlib import Path
from openpyxl import Workbook

db = DatabaseManager("expenses.db")


class Command:
    """ A protocol class that will be and example for implementing Commands """

    def execute(self, data):
        """ The actual execution of the command """
        pass


class CreateExpenseTableCommand:
    """ A command class that creates a SQL table """

    def execute(self):
        db.create_table(
            table_name="expenses", 
            columns={
            "id": "integer primary key autoincrement",
            "good": "text not null",
            "price": "integer not null",
            "date": "date" 
            }
        )


class AddExpenseCommand:
    """ A command class that inserts data into the SQL table"""

    def execute(self, data: dict):
        db.add(table_name="expenses", data=data)

        return "Expense added"

 
class ListsExpensesFirstCommand:
    """ A command class that will list expenses between a given date range in the SQL table """
 
    def execute(self, data:dict):
        start_date = data["start_date"]
        end_date = data["end_date"]

        criteria = {'between': ("date", start_date, end_date)}
        results = db.select('expenses', criteria=criteria, order_by="date", descending=True)
        total = 0
        for result in results:
            print(f"{result[1]}: ${result[2]}, {result[3]}")
            total +=result[2]
        print()

        return f"Total expenses: ${total}"
        
        
class ListsExpensesSecondCommand:
    """ 
    A command class that will list the expenses for a specific good value
    between a given date range in a SQL table 
    """
 
    def execute(self, data:dict):
        start_date = data["start_date"]
        end_date = data["end_date"]
        good = data["good"]

        criteria = {
            "between": ("date", start_date, end_date),
            "good" : good
            }
        
        results = db.select("expenses", criteria=criteria, order_by="date")
        total = 0
        for result in results:
            print(f"{result[1]}: ${result[2]}, {result[3]}")
            total += result[2]
          
        return f"Total expenses with {good}: ${total}"
    

class ListExpensesThirdCommand:
    """
     A command class that will return a list of tuples containing the good, 
     price and date for all rows that meet a comparison condition.
    """

    def execute(self, data: dict):
        price = data["price"]
        comparison_operator = data["comparison_operator"]

        criteria = {
            "comparison_operator":(comparison_operator,price) 
            }
        results = db.select("expenses", criteria=criteria)

        total = 0
        for result in results:
            print(f"Good: {result[1]}, Price: ${result[2]}, Date: {result[3]}")
            total += result[2]
          
        return f"Total expenses: ${total}"  
    

class EditExpenseCommand:
    """ A Command class that will edit an expense identified with an ID """

    def execute(self, data:dict):

        db.update(
            table_name="expenses", criteria={"id": data["id"]}, data=data["update"]
        )
        return "Expense updated!"
    

class DeleteExpenseCommand:
    """ A Command class that will delete an entry from the SQL table """

    def execute(self, data: int) -> str:
        db.delete_entry(table_name="expenses", criteria={"id": data})
        return "Entry deleted!"


class ExportToExcelCommand:
    """ A Command class used to export the data in Excel format """

    def execute(self, data: str) -> str:
        workbook = Workbook()
        worksheet = workbook.active
        results = db.select(table_name="expenses", order_by="id")
        
        for row in results:
            worksheet.append(row)

        export_folder_path = Path(f"./exports")
        export_folder_path.mkdir(parents=True, exist_ok=True)

        workbook.save(export_folder_path / f"{data}.xlsx")

        return f"Exported to file {data}"
    
    
class QuitCommand:
    """ A Command class that will quit the application """

    def execute(self):
        sys.exit()