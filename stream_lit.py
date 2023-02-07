# !pip install langchain
# !pip install PyPDF2
# !pip install faiss-cpu
# !pip install openai
# !pip install qdrant-client
# !pip install qdrant

import streamlit as st
import os
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]


from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain import OpenAI, VectorDBQA
from PyPDF2 import PdfReader
from langchain.chains.question_answering import load_qa_chain
st.set_page_config(page_title= "Chatur-GPT", page_icon="✨" , layout="centered", initial_sidebar_state="auto", menu_items=None)



st.title('Chatur GPT')

label='Upload the file that you want chatur to read'

filename= st.file_uploader(label, type ='pdf' )

print(filename)

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden; }
        footer:after {
	content:'Made with ❤️ by Mystic Labs'; 
	visibility: visible;
	display: block;
	position: relative;
	#background-color: red;
	padding: 5px;
	top: 2px;
}
        </style>
        



        """


st.markdown(hide_menu_style, unsafe_allow_html=True)





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

        
def newList():
    new_list=func(filename)
    embeddings = OpenAIEmbeddings()

    return new_list,embeddings

new_list,embeddings= newList()

if(new_list!=None):

    if(len(new_list)!=0):


        docsearch = FAISS.from_texts(new_list, embeddings)
        qa_chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")
        qa = VectorDBQA(combine_documents_chain=qa_chain, vectorstore=docsearch)


if 'output' not in st.session_state:
    st.session_state["output"] = ''

        


label1= 'Enter what you want to ask Chatur'
output2=''

def onclickfunc():
    global qa

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


if filename==None:
    st.session_state.output='Upload the file'
    

else:
    if new_list==None:
        new_list,embeddings=newList()
        

    else:
        if (filename!=None and len(new_list)==0):
                st.session_state.output='File is not readable'

            


        else:

            if qa==None:
                docsearch = FAISS.from_texts(new_list, embeddings)
                qa_chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")
                qa = VectorDBQA(combine_documents_chain=qa_chain, vectorstore=docsearch)
                print("last step")
            else:
                onclickfunc()





if (filename==None):
        st.session_state.output='Upload the file'
        
        


        if (filename!=None and new_list==None ):
            new_list,embeddings=newList()
            docsearch = FAISS.from_texts(new_list, embeddings)
            qa_chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")
            qa = VectorDBQA(combine_documents_chain=qa_chain, vectorstore=docsearch)
            onclickfunc()
            print('st1')


            if(filename!=None and docsearch==None):
                docsearch = FAISS.from_texts(new_list, embeddings)
                qa_chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")
                qa = VectorDBQA(combine_documents_chain=qa_chain, vectorstore=docsearch)
                onclickfunc()




        
            else:
                qa_chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")
                qa = VectorDBQA(combine_documents_chain=qa_chain, vectorstore=docsearch)
                onclickfunc()

        else:
            if(filename!= None and docsearch==None):
                docsearch = FAISS.from_texts(new_list, embeddings)
                qa_chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")
                qa = VectorDBQA(combine_documents_chain=qa_chain, vectorstore=docsearch)
                onclickfunc()




        
            # else:

            #     qa_chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")
            #     qa = VectorDBQA(combine_documents_chain=qa_chain, vectorstore=docsearch)
            #     onclickfunc()









# st.write("Chatur found out:\n", st.session_state["output"])
# output1= st.button('Ask Chatur', on_click= onclickfunc)

st.text_area('Chatur found out: ',value= st.session_state.output, disabled= True)

st.write("Tell us your usecase to build [Mail Us](mailto:f20200586@goa.bits-pilani.ac.in?subject=Loved%20your%20Chatbot!%20would%20like%20to%20make%20the%20same%20for%20my%20usecase&body=we%20can%20see%20a%20usecase%20in%20our%20product%20and%20would%20like%20to%20contact%20you%20on%20the%20same%0D%0Ahere%20is%20our%20usecase%3A%0D%0A%0D%0A)")

