# !pip install langchain
# !pip install PyPDF2
# !pip install faiss-cpu
# !pip install openai
# !pip install qdrant-client
# !pip install qdrant

import streamlit as st
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain import OpenAI, VectorDBQA
from PyPDF2 import PdfReader
from langchain.chains.question_answering import load_qa_chain


st.title('Chatur GPT')

label='Upload the file that you want chatur to read'

filename= st.file_uploader(label, type ='pdf' )

print(filename)
@st.cache
def func(filename):
    if(filename!=None):

        reader = PdfReader(filename)
        
        # printing number of pages in pdf file
        pdf_len = len(reader.pages)
        
        # getting a specific page from the pdf file
        final_text=''

        final_list=list()

        for i in range(pdf_len):
                page = reader.pages[i]
                text = page.extract_text()
                final = text.replace("\n"," ")
                final_text=final_text+text

                final_list.append(final)
        

        
        # extracting text from page

        new_list = list(filter(lambda x: x != '', final_list))
        # print(new_list)
        # print(len(new_list))
        return new_list

        

new_list=func(filename)
embeddings = OpenAIEmbeddings()

if(new_list!=None):
        docsearch = FAISS.from_texts(new_list, embeddings)


        qa_chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")
        qa = VectorDBQA(combine_documents_chain=qa_chain, vectorstore=docsearch)


if 'output' not in st.session_state:
    st.session_state["output"] = ''

        


label1= 'Enter what you want to ask Chatur'
output2=''

def onclickfunc():

    with st.spinner('Chatur is looking in the docs'):
    

        
        if(input1!=''):
            output2 = qa.run(input1)
            st.session_state["output"]= output2
            print(output2)
           
            
        

        else:
            output2='Please enter an input'
            st.session_state["output"]= output2

            print(output2)

    
    return output2

input1 = st.text_input(label1)
print(input1)
onclickfunc()

# st.write("Chatur found out:\n", st.session_state["output"])
# output1= st.button('Ask Chatur', on_click= onclickfunc)

st.text_area('Chatur found out: ',value= st.session_state.output, disabled= True)
