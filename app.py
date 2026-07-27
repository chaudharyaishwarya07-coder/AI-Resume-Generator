import streamlit as st 
# streamlit web based app making 
# lite python framework 
st.title("AI Resume Maker")  
st.markdown("""## user can create or 
download AI created resume based on high ATS Score""") 

# ==============AGENT CODE===========

import os
import time
import langchain
from  langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
import pytesseract as pyt
from tavily import TavilyClient
from langchain.messages import SystemMessage,HumanMessage
import numpy as np
import streamlit as st
from langchain_community.document_loaders import PyMuPDFLoader
GOOGLE_API_KEY=st.sidebar.text_input("GOOGLE_API_KEY ",type="password")
GROQ_APY_KEY=st.sidebar.text_input("GROQ_API_KEY",type="password")
TAVILY_API_KEY=st.sidebar.text_input("TAVILY_API_KEY",type="password") 
model=ChatGoogleGenerativeAI(
    model='gemini-3.5-flash-lite',
    google_api_key=GOOGLE_API_KEY
) 
prompt_generator(model)
def search_recent_news_jobs(query):
  """This function helps to search
  recent news or recent jobs
  related to given search query
  suppose user write Python Developer jobs
  It should return trending news and jobs link"""
  client=TavilyClient(
      api_key=TAVILY_API_KEY
  )
  return client.search(query)   

  # agent creation
from langchain.agents import create_agent

agent=create_agent(
    model=model,
    tools=[search_recent_news_jobs]

)    
# ====================promt generation ===================
prompt_generator(model)

def prompt_generation(agent):
  """This function helps to give detailed prompt
  followed by Chain of thoughts and
  persona based prompting, main task is to give
  detailed prompt to build Resume for
  students or Experienced person
  based on their given personal information.
  """
  prompt="""you are a senior HR resume analyzer,
  main tak is to give
  detailed prompt to build Resume  for
  students or Experienced person
  based on their given personal information.
  System Instruction I want model to generate resume
  in html format, include that in prompt
  """
  response=agent.invoke(prompt)
  file_name='prompt.py'
  with open(file_name,'w') as f:
    f.write(response.content[-1]['text'])
  return "prompt file generated Successfully,agent can read it" 

  def resumme_maker_prompt():
      """This function just gives
      updated prompt for model"""
  with open('prompt.py','r') as f:
    prompt=f.read()
  return prompt  
  #=====================generate resume=============== 

  prompt="""you are a heplful ai assistant
with jobs resume maker,your task is to give
html format resume with proper designing using
recent css, java script code, with professsional design format,
user will upload data and return HTML format resume
"""
final_prompt=prompt + resumme_maker_prompt()
user_details="""user details:given below:
Name: Aishwarya Chaudhary
I'm aishwarya chaudhary done my 11th and 12th from himalya public school
currently i am studying BCA from iitm. I am in 2nd year now
the languages right now i am learning is C,HTML,C++,PYTHON,PHP
"""

query=final_prompt + user_details 

if st.button("Generate Button"):
  with st.spinner("Running Agent..."):
    response = agent.invoke({'messages':[{'role':'user','content':query}]})
    code=response['messages'][-1].content[-1]['text']  

    #st.markdown(code)
    st.html(code,width="stretch",unsafe_allow_javascript=True)

