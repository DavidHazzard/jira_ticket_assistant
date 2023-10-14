import sqlalchemy as sa
from sqlalchemy import MetaData
from sqlalchemy import inspect
from urllib.parse import quote_plus

def build_connection_string(driver_name, user_id, password, server_name, db_name):
        return "mssql+pyodbc:///?odbc_connect={}".format(quote_plus(f"DRIVER={driver_name};SERVER={server_name};DATABASE={db_name};UID={user_id};PWD={password};TrustServerCertificate=yes"))
    
def get_engine(driver_name, user_id, password, server_name, db_name):
    return sa.create_engine(build_connection_string(driver_name, user_id, password, server_name, db_name))

def establishConnection():
    g_driver = "{ODBC Driver 18 for SQL Server}"
    g_user = "ai_playground@dhazzard-personal"
    g_password = "[insert_password_here]"
    g_host = "40.78.225.32"
    g_database = "dhazzard-ai-playground"
    try:
        engine = get_engine(g_driver, g_user, g_password, g_host, g_database)
        return engine
    except Exception as ex:
        print("Connection could not be made due to the following error: \n", ex)
        return None

def getMetaData(engine):
    if engine is not None:
        metadata = MetaData()
        metadata.reflect(bind=engine)
        return metadata
    else:
        raise ValueError("No engine has been established. Please establish an engine before attempting to get metadata.")

def getInspector(engine):
    if engine is not None:
        inspector = inspect(engine)
        return inspector
    else:
        print("No engine has been established. Please establish an engine before attempting to get an inspector.")
        return None   

def getDatabaseSchemaFromJson(inspector, json):
    schema_json = {}
    for table in json["tables"]:
        try:
            result = {
                "table": table,
                "columns": [c["name"] for c in inspector.get_columns(table)],
                "pk_constraint": inspector.get_pk_constraint(table),
                "foreign_keys": inspector.get_foreign_keys(table)
            }
            schema_json[table] = result
            print("\n")
        except Exception as ex:
            print(f"Table '{table}' does not exist in the current database. \n {ex} \n")
            schema_json[table] = None
        print(schema_json)
    return schema_json

class aiPlaygroundDatabase:
    def __init__(self):
        self.engine = establishConnection()
        self.metadata = getMetaData(self.engine)
        self.inspector = getInspector(self.engine)
    
