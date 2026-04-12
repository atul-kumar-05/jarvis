from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

def decide_next_action(tasks, memory):
    llm = ChatOllama(model="phi3")

    parser = JsonOutputParser()

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an elite AI productivity manager"),
        ("human", f"""
                    User Tasks:
                    {{tasks}}
                    
                    User Memory:
                    {{memory}}
                    
                    Rules:
                    - Pick ONE most important next action
                    - Be extremely specific
                    - Output must be short and actionable
                    
                    {parser.get_format_instructions()}
                    """)
                        ])

    chain = prompt | llm | parser

    result = chain.invoke({
        "tasks": tasks,
        "memory": memory
    })

    return result