import streamlit as st
import asyncio
import logging
import os
from uuid import uuid4                                                          #Neu Hinzugefügt
from src.chat_logger import save_chat_log                                       #Neu Hinzugefügt
from langchain.schema import ChatMessage
from src.chatbot import CustomChatBot

INDEX_DATA = os.environ.get("INDEX_DATA", "0")
PULL_EMBEDDING_MODEL = os.environ.get("PULL_EMBEDDING_MODEL", "0")

# Configure logger
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more details
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Console logs
    ],
)

logger = logging.getLogger(__name__)

logger.info(f"INDEX_DATA={INDEX_DATA}, PULL_EMBEDDING_MODEL={PULL_EMBEDDING_MODEL}")
# Initialize chatbot instance (avoid reloading)
if "bot" not in st.session_state:
    st.session_state["bot"] = CustomChatBot(index_data=True, 
                                            pull_embedding_model=False)



#-----------------------------------------
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid4())
    logger.info(f"New session_id created: {st.session_state['session_id']}")

#-----------------------------------------



# Streamlit UI setup
st.set_page_config(page_title="Phishinggpt", page_icon="📄")
st.header("Chat with your Document")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [ChatMessage(role="assistant", content="How can I help you?")]

if len(st.session_state["messages"]) == 0 or st.sidebar.button("Clear message history"):
    st.session_state["messages"].clear()
    st.session_state["messages"] = [ChatMessage(role="assistant", content="How can I help you?")]

# Display chat messages
for msg in st.session_state.messages:
    st.chat_message(msg.role).write(msg.content)

# Handle user input
if user_query := st.chat_input(placeholder="Ask me anything!"):
    # Usernachricht speichern & anzeigen
    st.session_state["messages"].append(ChatMessage(role="user", content=user_query))
    logger.info(f"Write user message in session state {user_query}")
    st.chat_message("user").write(user_query)

    # Assistentenantwort synchron holen
    with st.chat_message("assistant"):
        with st.spinner("Searching for information in your documents and generating response..."):
            try:
                answer = st.session_state["bot"].ask(user_query)
            except Exception as e:
                logger.error(f"Error processing query: {e}", exc_info=True)
                st.error("An error occurred while processing your request.")
                answer = ""

        # Antwort anzeigen & in Verlauf schreiben
        if answer:
            st.markdown(answer)
            st.session_state.messages.append(
                ChatMessage(role="assistant", content=answer)
            )

            # 👇 Logging in Datei
            try:
                save_chat_log(
                    session_id=st.session_state["session_id"],
                    user_message=user_query,
                    bot_reply=answer,
                    meta={
                        "source": "streamlit",
                        "model": os.environ.get("MODEL_NAME", "llama3.2:1B"),
                        "collection": os.environ.get("CHROMA_COLLECTION_NAME", "AI_Book"),
                    },
                )
                logger.info("Chat log successfully saved.")
            except Exception as log_err:
                logger.error(f"Error while saving chat log: {log_err}", exc_info=True)
