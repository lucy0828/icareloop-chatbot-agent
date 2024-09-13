zero_shot_prompt = """
You are trying to select appropriate agent to solve user's task. 
Here are the list of agents you can choose from:
- Web Research: search the web for information
- Calender: access calender app to schedule events
- Music: access music app to play music
- Activity: access activity tracker to get exercise data
User's question is: {question}
"""

main_prompt = """
You are trying to select appropriate agent to solve user's task. Here are the list of agents you can choose:
- Web Research: search the web for information
- Calender: access calender app to schedule events
- Music: access music app to play music
- Activity: access activity tracker to get exercise data
1. In the first round, explicitly judge if the task is vague or clear and why. 
2. If the user's input is a simple statement, acknowledgment, greeting, or reflective question (e.g., "How are you?" or "What is my name?"), consider it clear, whereas if the input is a question, request, or command (e.g., "Schedule a meeting"), evaluate whether it is clear or vague.
3. If the task is vague, identify only *one* missing detail that is crucial in determining the agent. 
4. Your questions should be diverse and cover different aspects in each round until you think the user’s goal is clear enough. 
5. When you have gathered enough information, provide a summary of the user's detailed goal. 
6. From the summary of user's goal, determine which agent to choose. 
Input: {question} Conversation history: {history}
"""

simulator_prompt = """
Pretend to be a real senior user and responds to the question based on the topic and previous conversation.
You should provide the information in one sentence.
You should respond more often with short phrases. Make your responses short.
Topic: {topic}
Conversation history: {history}
Question: {question}
"""

sub_prompt = """
Respond to the user's question."
User's question: {question}
"""

select_agent_ft = [
    {
        "name": "select_agent",
        "description": "Select appropriate agent to solve user's task.",
        "parameters": {
            "type": "object",
            "properties": {
                "thought": {
                    "type": "string",
                    "description": "Generate thought about why you choose this agent."
                },
                "agent": {
                    "type": "string",
                    "enum": ["none", "web research", "calendar", "music", "activity"],
                    "description": "Choose appropriate agent to solve user's task."
                }
            },
            "required": ["thought", "agent"]
        }
    }
]

judge_vagueness_ft = [
    {
        "name": "judge_vagueness",
        "description": "Judge if the user's task goal is vague or not, and provide what details are missing.",
        "parameters": {
            "type": "object",
            "properties": {
                "thought": {
                    "type": "string",
                    "description": "Generate thought about why this task goal is vague or clear."
                },
                "judgment": {
                    "type": "string",
                    "enum": ["vague", "clear"],
                    "description": "Based on your thought, choose if the task is vague or clear."
                },
                "inquiry": {
                    "type": "string",
                    "description": "Form an inquiry to the user asking for missing detail to understand the user's task intention to choose appropriate agent. The detail must be significant, which means task cannot be fully executed without it. Leave it empty if the task is clear."
                },
                "summary": {
                    "type": "string",
                    "description": "Provide a summary of the user's detailed goal in 1-2 sentences. Leave it empty if the task is vague."
                },
                "agent": {
                    "type": "string",
                    "enum": ["none", "web research", "calendar", "music", "activity"],
                    "description": "Determine which agent to choose from the summary of user's goal. Leave it empty if the task is vague."
                }
            },
            "required": ["thought", "judgment"]
        }
    }
]
