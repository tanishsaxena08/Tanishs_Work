# # Step1 : Setup UI with streamlit (model provider, modelm system prompt, web_search query)
# import streamlit as st

# st.set_page_config(page_title="LangGraph Agent UI", layout="wide", page_icon="🤖")
# st.title("🤖 LangGraph AI Chatbot Agent")
# st.write("Create and Interact with AI agents")

# system_prompt = st.text_area("Define yout AI Agent: ", height = 70, placeholder="Type your system prompt here...")

# MODEL_NAMES_GROQ = ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]
# MODEL_NAMES_OPENAI = ["gpt-4o-mini"]

# provider = st.selectbox("Select Model Provider: ", ["Groq", "OpenAI"])

# if provider == "Groq":
#     selected_model = st.selectbox("Select Groq Model: ", MODEL_NAMES_GROQ)
# elif provider == "OpenAI":
#     selected_model = st.selectbox("Select OpenAI Model: ", MODEL_NAMES_OPENAI)

# allow_web_search = st.checkbox("Allow Web Search Tool", value=False)

# user_query = st.text_area("Enter your query: ", height = 150, placeholder="Ask Anything...")

# API_URL = "http://127.0.0.1:9999/chat"

# if st.button("Ask AGent!"):
#     if user_query.strip():
#         # Step2 : Connect with backend via URL
#         import requests

#         payloads = {
#             "model_name": selected_model,
#             "model_provider": provider,
#             "system_provider": system_prompt,
#             "messages": [user_query], #user query will be passed as list
#             "allow_search": allow_web_search}
        
#         response = requests.post(API_URL, json=payloads)
#         if response.status_code == 200:
#             response_data = response.json()
#             if "error" in response_data:
#                 st.error(f"Error: {response_data['error']}")
#             else:
#                 #Get response from backend and show here
#                 # response = "Hi, This is a fixed dummy response from backend!"
#                 st.subheader("Agent Response")
#                 st.markdown(f"**Final Response:** {response_data['response']}")

import streamlit as st
import requests

st.set_page_config(page_title="LangGraph Agent UI", layout="wide", page_icon="🤖")
st.title("🤖 LangGraph AI Chatbot Agent")
st.write("Create and Interact with AI agents")

system_prompt = st.text_area("Define your AI Agent:", height=70, placeholder="Type your system prompt here...")

MODEL_NAMES_GROQ = ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]
MODEL_NAMES_OPENAI = ["gpt-4o-mini"]

provider = st.selectbox("Select Model Provider:", ["Groq", "OpenAI"])

if provider == "Groq":
    selected_model = st.selectbox("Select Groq Model:", MODEL_NAMES_GROQ)
elif provider == "OpenAI":
    selected_model = st.selectbox("Select OpenAI Model:", MODEL_NAMES_OPENAI)

allow_web_search = st.checkbox("Allow Web Search Tool", value=False)

user_query = st.text_area("Enter your query:", height=150, placeholder="Ask Anything...")

API_URL = "http://127.0.0.1:9999/chat"

if st.button("Ask Agent!"):
    if user_query.strip():
        payloads = {
            "model_name": selected_model,
            "model_provider": provider,
            "system_provider": system_prompt,
            "messages": [user_query],
            "allow_search": allow_web_search
        }

        try:
            with st.spinner("Thinking..."):
                response = requests.post(API_URL, json=payloads)
                response.raise_for_status()
                response_data = response.json()

            if "error" in response_data:
                st.error(f"Error: {response_data['error']}")
            elif "response" in response_data:
                st.subheader("Agent Response")
                st.markdown(f"**Final Response:** {response_data['response']}")
            else:
                st.warning("Unexpected response format from backend.")
        except requests.exceptions.ConnectionError:
            st.error("❌ Could not connect to backend. Is FastAPI running?")
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Request failed: {e}")
    else:
        st.warning("Please enter a query before submitting.")