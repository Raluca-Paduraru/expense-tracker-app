# Expense Tracker 

## Setting up the virtual environment

```
> python -m venv .venv
```

## Activating the virtual environment

### On Windows
```
> .venv\Scripts\activate
```

## Deactivating the virtual environment

```
> deactivate
```

## Features

- Add and keep track of expenses in a SQL database
- Search and filter expenses
- Export data to Excel

## Architecture

The project is divided into three layers:

1. Storage layer (`database.py`): responsible for managing the persistence of data in a SQL database.
2. Business logic layer (`command.py`): responsible for implementing the core functionality of the application.
3. Presentation layer (`presentation.py`): responsible for interacting with the user and displaying the results.

## Usage

The project is run from `expense_tracker.py`. To use the application, simply run the script and follow the prompts.