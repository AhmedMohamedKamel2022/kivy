import pyodbc

SERVER  = 'DESKTOP-SBIP543'
DATABASE = "FactoryMaintenancePro"

connection_string = (
    f"DRIVER={{SQL Server}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    "Trusted_Connection=yes;"
)

def get_connection():
    return pyodbc.connect(connection_string)