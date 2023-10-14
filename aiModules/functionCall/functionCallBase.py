from aiModules import openAIBase as oai
import json
from aiModules.templates import ticketBaseTemplates as tt
from langchain.chat_models import ChatOpenAI

oai.setAIKeyFromEnvVariables()
local_ai = oai.ai

def getFunctionDefinition(functionString, ticketType):
    name = f"get{functionString}Template"
    description = f"Get the template for a {ticketType} ticket"
    parameters = {
        "type": "object",
        "properties": {
            "client": {
                "type": "string",
                "description": "The shortname of the client for whom the user story is being written"
            },
            "role": {
                "type": "string",
                "description": "The role of the stakeholder for whom the user story is being written"
            },
            "ticket_type": {
                "type": "string",
                "description": "The type of ticket being written"
            },
            "result_type": {
                "type": "string",
                "description": "The type of result being generated by the ticket"
            }
        },
        "required": [],
    }
    
    return {
        "name": name,
        "description": description,
        "parameters": parameters,
    }


def getTemplateFromFunctionCall(prompt):
    messages = [{"role": "user", "content": prompt}]
    functions = [
        getFunctionDefinition("UserStory", "user story"),
        getFunctionDefinition("BugReport", "bug report"),
        getFunctionDefinition("TestPlan", "test plan"),
        getFunctionDefinition("TestCases", "test cases"),
        getFunctionDefinition("DbQuery", "database query"),
        getFunctionDefinition("RegressionRisk", "regression risk")
    ]
    response = local_ai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",
    )
    response_message = response["choices"][0]["message"]

    if response_message.get("function_call"):
        available_functions = {
            "getUserStoryTemplate": tt.getUserStoryTemplate,
            "getBugReportTemplate": tt.getBugReportTemplate,
            "getTestPlanTemplate": tt.getTestPlanTemplate,
            "getTestCasesTemplate": tt.getTestCasesTemplate,
            "getDbQueryTemplate": tt.getDbQueryTemplate,
            "getRegressionRiskTemplate": tt.getRegressionRiskTemplate
        }
        function_name = response_message["function_call"]["name"]
        function_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = function_to_call(**function_args)

        messages.append(response_message)
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )
        print(messages)
        return runTemplateFromFunctionCall(function_response)
    
def runTemplateFromFunctionCall(func_response):
    chat = ChatOpenAI(openai_api_key=oai.ai.api_key)
    print(func_response)
    response = chat(func_response)
    print(response)
    func_response.append(response)
    return func_response