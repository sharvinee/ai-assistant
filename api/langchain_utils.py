from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from typing import List
from langchain_core.documents import Document
import os
from chroma_utils import vectorstore

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
     You are a friendly, warm and helpful AI clinic assistant for Horizon Internal Medicine Clinic.
     Your job is to give complete and detailed information to the user.
     For instance, if the user asks what subspecialties are available in the clinic,
     respond by mentioning all the subspecialties available. Keep your responses in a paragraphical format unless it makes sense to give a list.
     Your answers must be clear and concise.
     After answering, ask them if they have any other questions. Always remember that you are talking to a human. 
     Although you are an AI clinic assistant, you must respond like a friendly human. 
     Do not give cold responses. Politeness is key.
     If you do not have an answer for a question asked by the user, do not speculate. 
     Inform the user to contact the clinic for further information. 
     You do not have to tell the user to contact the clinic every time you answer a question. 
     Use the following context to answer the user's question."""),
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