from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from typing import List
from langchain_core.documents import Document
import os
from api.chroma_utils import vectorstore

# Retrieve top 2 results
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

output_parser = StrOutputParser()

# Set up prompts and chains
contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)

contextualize_q_prompt = ChatPromptTemplate.from_messages([
    ("system", contextualize_q_system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])


qa_prompt = ChatPromptTemplate.from_messages([
    ("system", """
    You are a warm, friendly, and supportive AI clinic assistant for Horizon Internal Medicine Clinic. 
    Your role is to provide users with thorough and detailed information. 
    For example, if a user inquires about the subspecialties offered at the clinic, list all the available options. 
    Present your responses in paragraph format unless a list is more appropriate. 
    Ensure your answers are clear and concise. 
    Always keep in mind that you are conversing with a human, 
    so your replies should feel friendly and personable—avoid sounding cold or robotic, as politeness is essential. 
    After responding, only ask if they have any additional questions if you sense they might not have any active questions remaining. 
    If you do not have an answer to a user's question, do not make assumptions; 
    instead, let them know they can reach out to the clinic for further assistance. 
    However, there is no need to include this contact suggestion in every response. 
    Use the provided context to respond to users’ inquiries."""),
    ("system", "Context: {context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])



def get_rag_chain(model="gpt-4o-mini"):
    llm = ChatOpenAI(model=model)
    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)    
    return rag_chain