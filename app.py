# Importing required packages
import streamlit as st
from langchain_openai import OpenAI
import promptlayer
import uuid

MODEL = "gpt-3.5-turbo-16k"

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    
st.set_page_config(page_title="Learn Wardley Mapping")
st.sidebar.title("Learn Wardley Mapping")
st.sidebar.image("./logo.png")
st.sidebar.markdown("Developed by Mark Craddock](https://twitter.com/mcraddock)", unsafe_allow_html=True)
st.sidebar.markdown("Current Version: 0.0.3")
st.sidebar.divider()
#st.sidebar.markdown("Using gpt-4-1106-preview API")
#st.sidebar.markdown(st.session_state.session_id)
#st.sidebar.divider()

# Check if the user has provided an API key, otherwise default to the secret
user_openai_api_key = st.sidebar.text_input("Enter your OpenAI API Key:", placeholder="sk-...", type="password")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = MODEL

if user_openai_api_key:
    # If the user has provided an API key, use it
    # Swap out openai for promptlayer
    promptlayer.api_key = st.secrets["PROMPTLAYER"]
    openai = promptlayer.openai
    openai.api_key = user_openai_api_key
else:
    st.warning("Please enter your OpenAI API key", icon="⚠️")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
            "role": "system",
            "content": f"""
             Interact with LearnWardleyMappingBot, your personal guide to learning and creating Wardley Maps.
             Discover the power of Wardley Mapping for strategic planning and decision-making by choosing to 'Learn' about the components of a Wardley Map, or 'Vocabulary' and I will provide a list of common terms and their definitions. or 'Create' your own map with step-by-step guidance.
             If you need assistance, type 'Help' for support. Begin your Wardley Mapping journey now!
             """
        })
    st.session_state.messages.append(   
        {
            "role": "user",
            "content": "Help?"
        })
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": """
            I'm here to help you learn about and create Wardley Maps. Here are some options for getting started:
            1. Learn: To learn about the components and concepts of a Wardley Map, type "Learn".
            2. Vocabulary: To get a list of common Wardley Map terms and their definitions, type "Vocabulary".
            3. Create: To create your own Wardley Map with step-by-step guidance, type "Create".
            If you have any specific questions or need clarification on any aspect of Wardley Mapping, feel free to ask.
            """
        })

for message in st.session_state.messages:
    if message["role"] in ["user", "assistant"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if user_openai_api_key:
    if prompt := st.chat_input("How can I help with Wardley Mapping?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
    
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
                pl_tags=["learnwardleymapping", st.session_state.session_id],
            ):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
