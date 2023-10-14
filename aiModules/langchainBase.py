import os
import langchain
from aiModules import openAIBase as oai
from langchain import *
from langchain.chat_models import ChatOpenAI
from aiModules.functionCall.functionCallBase import getTemplateFromFunctionCall as getBaseTemplate
from aiModules.functionCall.functionCallOutput import getTemplateFromFunctionCall as getOutputTemplate
from aiModules.templates import ticketBaseTemplates as tt

oai.setAIKeyFromEnvVariables()

def initializeChatTemplate(self):
    ai_template = tt.getAITemplate()
    prompt = input(f"{ai_template}: ")
    self.template_history = getBaseTemplate(prompt)
    self.chain.run("")

def getIntroMessage(template):
    default_message = "Please provide me some information about the ticket you would like to write: "
    try:
        intro_message = template["choices"][0]["message"]["content"].split(" ", 1)[1]
        return intro_message
    except:
        return default_message

def exitConversationChain(message_list, ticketOutputs):
    if len(message_list) > 0:
        ticket_output = getOutputTemplate(message_list)
        ticketOutputs.append(ticket_output)
        return ticket_output.content
    else:
        print("No content generated")
        return None

def run(self):
    self.chainActive = True
    while self.chainActive:
        try:
            if self.template_history == None:
                initializeChatTemplate(self)
            else:
                if len(self.chain.memory.chat_memory.messages) == 0:
                    intro_message = getIntroMessage(self.template)
                    prompt = input(f"{intro_message} ")
                else:
                    prompt = input(f"{self.chain.memory.chat_memory.messages[-1].content}")
                if prompt == "exit":
                    print("Exiting...")
                    self.chainActive = False
                    return exitConversationChain(self.chain.memory.chat_memory.messages, self.ticketOutputs)
                else:
                    self.chain.run(prompt)
                    print("Human: " + self.chain.memory.chat_memory.messages[-2].content)
                    print("AI: " + self.chain.memory.chat_memory.messages[-1].content)
        except KeyboardInterrupt:
            pass
    return self.chain

class ticketAssistant_lc:
    def __init__(self):
        self.llm = OpenAI(openai_api_key=oai.ai.api_key, temperature="0.7")
        self.chat = ChatOpenAI(openai_api_key=oai.ai.api_key, temperature="0.7")
        self.template_history = None
        self.chain = ConversationChain(llm=self.llm, verbose=False)
        self.chainActive = False
        self.ticketOutputs = []
    def run_blind(self):
        if self.chain.memory.chat_memory.messages != []:
            self.chain = ConversationChain(llm=self.llm, verbose=False)
        run(self)
    def run_context(self):
        run(self)
