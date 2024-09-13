import os
from dotenv import load_dotenv
from typing import TypedDict
from langchain_openai import ChatOpenAI
from langchain_ollama.llms import OllamaLLM
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langgraph.graph import END
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from eval_template import *


load_dotenv()
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
output_parser = StrOutputParser()

# Main configuration
main_model = ChatOpenAI(model="gpt-3.5-turbo")
# main_model = OllamaLLM(model="mistral-nemo")
# main_model = ChatNVIDIA(model="nv-mistralai/mistral-nemo-12b-instruct",
#                         api_key=NVIDIA_API_KEY)
main_template = ChatPromptTemplate.from_template(main_prompt)
main_agent = main_template | main_model | output_parser

# Agent configuration
# agent_model = OllamaLLM(model="mistral-nemo")
agent_model = ChatOpenAI(model="gpt-3.5-turbo")
# agent_model = ChatNVIDIA(model="nv-mistralai/mistral-nemo-12b-instruct",
#                          api_key=NVIDIA_API_KEY)

info_template = ChatPromptTemplate.from_template(info_prompt)
info_agent = info_template | agent_model | output_parser


class EvalAgent(TypedDict):
    question: str
    reference: str
    main_msg: str
    agent_msg: str


def main_node(state: EvalAgent):
    question = state["question"]
    main_response = main_agent.invoke({"question": question})
    return {"main_msg": main_response}


def info_agent_node(state: EvalAgent):
    question = state["question"]
    info = state["reference"]
    agent_response = info_agent.invoke({"info": info, "question": question})
    return {"agent_msg": agent_response}


def _plan_route(state):
    if state["main_msg"] == "_call_info_agent":
        return "info_agent_node"
    else:
        return END
