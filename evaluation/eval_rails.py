import os
from dotenv import load_dotenv
from typing import TypedDict
from langchain_openai import ChatOpenAI
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from eval_template_userIntent import *
from nemoguardrails import RailsConfig, LLMRails
from nemoguardrails.integrations.langchain.runnable_rails import RunnableRails

load_dotenv()
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
str_parser = StrOutputParser()

sub_config = RailsConfig.from_path("./guardrails/config_sub")
sub_guardrails = RunnableRails(sub_config)
sub_model = ChatNVIDIA(model="nv-mistralai/mistral-nemo-12b-instruct",
                         api_key=NVIDIA_API_KEY)
sub_template = ChatPromptTemplate.from_template(sub_prompt)
sub_agent = sub_template | (sub_guardrails | sub_model) | str_parser
# sub_agent = sub_template | sub_model | str_parser


class EvalAgent(TypedDict):
    question: str
    sub_response: str


def sub_node(state: EvalAgent):
    question = state["question"]
    sub_response = sub_agent.invoke({"question": question})
    return {"sub_response": sub_response}

