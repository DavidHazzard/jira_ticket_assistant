import os
import openai as ai

def setAIKeyFromEnvVariables():
    ai.api_key = os.getenv("OPENAI_API_KEY_GPT4")
    ai.organization = os.getenv("OPENAI_ORG")

 
