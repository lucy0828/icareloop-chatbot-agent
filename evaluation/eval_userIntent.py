from dotenv import load_dotenv
from typing import TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import END
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers.openai_functions import JsonOutputFunctionsParser
from eval_template_userIntent import *

load_dotenv()
json_parser = JsonOutputFunctionsParser()
str_parser = StrOutputParser()

main_model = ChatOpenAI(model="gpt-4o")
main_template = ChatPromptTemplate.from_template(main_prompt)
main_agent = main_template | main_model.bind_functions(judge_vagueness_ft) | json_parser

simulator_model = ChatOpenAI(model="gpt-4o")
simulator_template = ChatPromptTemplate.from_template(simulator_prompt)
simulator = simulator_template | simulator_model | str_parser


class EvalAgent(TypedDict):
    topic: str
    question: str
    user_intent: dict
    simulator: str
    history: str


def main_node(state: EvalAgent):
    question = state["question"]
    history = state.get("history") or ""
    main_response = main_agent.invoke({"question": question, "history": history})
    return {"user_intent": main_response}


def simulator_node(state: EvalAgent):
    topic = state["topic"]
    inquiry = state["user_intent"].get("inquiry", "")
    history = state.get("history") or ""
    response = simulator.invoke({"topic": topic, "question": inquiry, "history": history})
    history += f"\nBot: {inquiry}\nUser: {response}"
    return {"simulator": response, "history": history}


def _route(state):
    judgment = state["user_intent"].get("judgment")

    if judgment == "vague":
        return "simulator_node"
    else:
        return END

