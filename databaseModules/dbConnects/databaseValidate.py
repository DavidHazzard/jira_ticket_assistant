from databaseModules.dbConnects import azureDatabaseConnect as adc
import sys
from databaseModules.functionCall.functionCallValidate import validateQueryFromFunctionCall

def establishDbConnection():
    az_db = adc.aiPlaygroundDatabase()
    if az_db.engine is not None:
        print("Database connection established.")
        try:
            az_db.metadata.tables.values()
            az_db.inspector.get_table_names()
            print("Successfully retrieved metadata and inspector.")
        except:
            print("Internal engine error.")
    else:
        print("No database connection.")
    return az_db

db = establishDbConnection()
validated_queries = []

def validateQueries(query_list):
    global validated_queries
    for query in query_list:
        if query.text.lower().startswith("select"):
            with db.engine.begin() as conn:
                try:
                    conn.execute(query)
                    validated_queries.append(query)
                except:
                    ex = str(sys.exc_info()[1])
                    print(f"Query '{query}' could not be run. \n {ex} \n")
                    validated_query = validateQueryFromFunctionCall(ex, query)
                    query_list.append(validated_query)
                    continue
    return validated_queries