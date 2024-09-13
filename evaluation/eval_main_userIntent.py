from langsmith import Client
from langsmith.evaluation import evaluate
from langgraph.graph import StateGraph, END
from eval_userIntent import *
from eval_userIntent import _route


client = Client()

graph = StateGraph(EvalAgent)
graph.add_node("main_node", main_node)
graph.add_node("simulator_node", simulator_node)
graph.add_conditional_edges("main_node", _route)
graph.add_edge("simulator_node", "main_node")
graph.add_edge("main_node", END)
graph.set_entry_point("main_node")
chatbot = graph.compile()

data = "test"
experiment_prefix = "test"


def predict_answer(example: dict):
    for s in chatbot.stream({"topic": example["topic"], "question": example["task"]}):
        print(s)
        print("------------------------")

        agent = "none"
        for key in s:
            if 'user_intent' in s[key]:
                agent = s[key]['user_intent'].get("agent", "error")

    return {"agent": agent}


def vagueness_evaluator(run, example) -> dict:
    label = example.outputs["vagueness"]
    prediction = run.outputs["vagueness"]
    if prediction == label:
        score = 1
    else:
        score = 0
    return {"score": score}


results = evaluate(
    predict_answer,
    data=data,
    # evaluators=[vagueness_evaluator],
    experiment_prefix=experiment_prefix,
)
