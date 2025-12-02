'''
Grok : Grok is a conversational AI assistant and large language model (LLM) from Elon Musk's xAI company, known for its witty personality, 
access to real-time information from the X platform (formerly Twitter), and a willingness to answer controversial questions.

Grok cloud : The AI inference platform built for developers. Fast responses, scalable performance, and costs you can plan for. 
Available in public, private, or co-cloud instances.

What is Tavily?
Tavily is a search API specifically designed for AI agents and applications like large language models (LLMs).
It works by providing real-time, factual information from the web to improve the accuracy and reliability of AI-generated content, 
which is especially useful for workflows like Retrieval Augmented Generation (RAG). Unlike traditional search APIs, Tavily aggregates and 
filters results from multiple sources to deliver concise, ready-to-use content for AI systems. 

OpenAI??
OpenAI is an American artificial intelligence research and deployment company with a mission to ensure that artificial general intelligence benefits all of humanity. 
It is known for developing advanced AI models like the GPT series and creating widely-used products such as ChatGPT

Langraph ??
LangGraph is an open-source framework for building robust, stateful AI agent applications using a graph-based architecture. Developed by the creators of LangChain, 
it provides a low-level orchestration layer that allows developers to define complex workflows with conditional logic, loops (cycles), and
the ability for multiple AI agents to collaborate. 

• ChatGroq → connects to Groq’s LLM service.
• ChatOpenAI → connects to OpenAI’s GPT models.
• TavilySearch → a search tool for retrieving web results.
• create_react_agent → builds a ReAct‑style agent (reason + act loop).
• AIMessage → represents AI responses in LangChain’s message format.
'''

#Step1 : Setup API keys for Grok. OpenAI and Tavily
# CODE STARTS HERE
from dotenv import load_dotenv
load_dotenv()

import os
import warnings

# Suppress warnings (Deprecation, UserWarning, etc.)
warnings.simplefilter("ignore")

# Step 1: Setup API Keys
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Warn if keys are missing
if not OPENAI_API_KEY:
    print("⚠️ OPENAI_API_KEY not set in environment")
if not GROQ_API_KEY:
    print("⚠️ GROQ_API_KEY not set in environment")
if not TAVILY_API_KEY:
    print("⚠️ TAVILY_API_KEY not set in environment")

# Step 2: Setup LLMs & Tools
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage

system_prompt = "Act as an AI chatbot who is smart and friendly"

def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider):
    # Choose LLM
    if provider == "Groq":
        llm = ChatGroq(model=llm_id)
    elif provider == "OpenAI":
        llm = ChatOpenAI(model=llm_id)

    # Add tools if allowed
    tools = [TavilySearch(max_results=2)] if allow_search else []

    # Create agent (no system_prompt/state_modifier here)
    agent = create_react_agent(
        model=llm,
        tools=tools,
    )

    # Inject system prompt at runtime
    state = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
    }

    try:
        response = agent.invoke(state)
        messages = response.get("messages", [])
        ai_messages = [m.content for m in messages if isinstance(m, AIMessage)]
        return ai_messages[-1] if ai_messages else "No AI response."
    except Exception as e:
        return f"❌ Error from agent: {e}"

if __name__ == "__main__":
    # Example 1: Groq + Tavily
    query = "Who won the FIFA World Cup 2022?"
    response = get_response_from_ai_agent(
        llm_id="llama-3.3-70b-versatile",
        query=query,
        allow_search=True,
        system_prompt=system_prompt,
        provider="Groq"
    )
    print("Response from Groq LLM with Search Tool:")
    print(response)

    # Example 2: OpenAI only
    # query2 = "Explain the theory of relativity."
    # response2 = get_response_from_ai_agent(
    #     llm_id="gpt-4o-mini",
    #     query=query2,
    #     allow_search=False,
    #     system_prompt=system_prompt,
    #     provider="OpenAI"
    # )
    # print("\nResponse from OpenAI LLM without Search Tool:")
    # print(response2)