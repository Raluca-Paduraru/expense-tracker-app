import commands as c
import presentation as p


def loop():
    options = {
        "A": p.Option(
            name="Add an expense", 
            command=c.AddExpenseCommand(),
            prep_call=p.get_new_expense_data
            ),
        "B": p.Option(
            name="Lists expenses by a given date range", 
            command=c.ListsExpensesFirstCommand(),
            prep_call=p.get_date_expense
            ),
        
        "C": p.Option(
            name="Lists total expenses by a good name", 
            command=c.ListsExpensesSecondCommand(),
            prep_call=p.get_good_value
            ),
        "O": p.Option(
            name="Lists all goods compared to a price value",
            command=c.ListExpensesThirdCommand(),
            prep_call=p.get_price_and_operator
            ),
        "D": p.Option(
            name="Delete an entry by id",
            command=c.DeleteExpenseCommand(),
            prep_call=p.get_expense_id
            ),
        "E": p.Option(
            name="Edit a bookmark",
            command=c.EditExpenseCommand(),
            prep_call=p.get_update_expense_data,
            ),
        "X": p.Option(
            name="Export to Excel",
            command=c.ExportToExcelCommand(),
            prep_call=p.get_file_name,
            ),
        "Q":p.Option(
            name="Quit",
            command=c.QuitCommand()
            )
    }

    p.clear_screen()
    p.print_options(options)
    chosen_option = p.get_option_choice(options)
    p.clear_screen()
    chosen_option.choose()
    
    
    _ = input("Press ENTER to return to menu")
    
if __name__ == "__main__":
    c.CreateExpenseTableCommand().execute()

    while True:
        loop()