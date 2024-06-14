from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.utilities import SQLDatabase
import streamlit as st 


def init_db(user,password,host,port,database):
    db_uri = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
    return SQLDatabase.from_uri(db_uri)

def get_sql_chain(db):
    template="""
    You are a data analyst at a comapny. You are interacting with a user who is asking your question about the company's database.
    Based on the table schema below, write a SQL query that would answer the user's question. Take the conversation history into account.
    
    <SCHEMA>{schema}</SCHEMA>
    
    Conversation History: {chat_history}
    
    Write only the SQL query and nothing else. Do not wrap the SQL query in any other text, not even backticks.
    
    for example:
    Question: which 3 artists have the most tracks?
    SQL Query: SELECT ArtistId, COUNT(*) FROM tracks GROUP BY ArtistId ORDER BY COUNT(*) DESC LIMIT 3;
    Question: Name 10 artists
    SQL Query: SELECT Name FROM artists LIMIT 10;
    
    Your turn:
    
    Question: {question}
    SQL Query:
    """
    
    

if  "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [
        AIMessage("Hello! I am a SQL Assistant. How can I help you?, Ask me anything, about your database...."),    
    ]

load_dotenv()

st.set_page_config(page_title="Chat with MySql",page_icon=":speech_balloon:")

st.title("Chat with MySql")

with st.sidebar:
    st.subheader("Settings")
    st.write("This is a chat app that uses a MySql database to store messages.")
    
    st.text_input("Host", value="localhost", key="Host")
    st.text_input("Port", value="3306",key="Port")
    st.text_input("user", value="root",key="User")
    st.text_input("Password",type="password", value="admin", key="Password")
    st.text_input("Database", value="Chinook", key="Database")
    
    if st.button("Connect"):
        with st.spinner("Connecting to the database....."):
            db = init_db(
                st.session_state["User"],
                st.session_state["Password"],
                st.session_state["Host"],
                st.session_state["Port"],
                st.session_state["Database"]
            )
            st.session_state.db=db
            st.success("Connected to the database!")
            
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.markdown(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)
            
user_query = st.chat_input("Type your message....")

if user_query is not None and user_query.strip() != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    
    with st.chat_message("Human"):
        st.markdown(user_query)
    
    with st.chat_message("AI"):
        response = "I don't know how to response to that...."
        st.markdown(response)
        st.session_state.chat_history.append(AIMessage(content=response))