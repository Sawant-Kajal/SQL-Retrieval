import mysql.connector as mysql
from mysql.connector import Error
import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()  # Load environment variables
#######################################################################################
genai.configure(api_key="API KEY") # Gemini LLM(Large Learning Model)
server = "127.0.0.1"
database = "ATS_resume"
username = "root"
password = "xyz@123"
#######################################################################################

def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

#######################################################################################

def retrieve_data(server, database, username, password, query):
    # Connect to the MySQL database
    try:
        con = mysql.connect(
            host=server,
            database=database,
            user=username,
            password=password
        )
        cursor = con.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Error as ex:
        print("Error connecting to database:", ex)
        return None

#######################################################################################

prompt = [
    """
    You are an expert in converting English questions to SQL query! and very professional sql developer like to perform advanced queries,
    you should know how human can call different things by various name so keep it in mind example Title can be known as Name
    The SQL database has the name ats_resume, having table imdb and has the following columns - [Title],[Year],[Total_episodes],
    [Rating],[Vote_count],[Category]
    \n\nFor example,\nExample 1 - How many Title are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM imdb ;
    \nExample 2 - Tell me all the Total_episodes having Total_episodes is less than 25?, 
    the SQL command will be something like this SELECT * FROM imdb 
    where Total_episodes >25"; 
    \nExample 3 - How many Title are there whose Year is more than 2018 then the sql command should be like SELECT * FROM imdb WHERE Year>=2015 perform this for similar prompts
    also the sql code should not have ```(' in beginning or end and sql word in output

    """
]

#######################################################################################
st.set_page_config(page_title="SQL-Retrieval")  # st.title(':rainbow[RESUME SPECTRUM]')
# Add a header with a teal color gradient
st.markdown(
    f'<h1 style="background-image: linear-gradient(to right,#e3f988, #9ab973, #8a9a5b, #4a5d23); 
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;">SQL-Retrieval</h1>',
    unsafe_allow_html=True
)

question = st.text_input("Input: ", key="input")

submit = st.button("Submit")

# if submit is clicked
if submit:
    response = get_gemini_response(question, prompt)
    print(response)

    response1 = retrieve_data(server, database, username, password, response)
    if response1 is not None:  # Check if response1 is not None
        st.subheader("The Response is")
        for row in response1:
            st.markdown(str(row))
    else:
        st.error("Couldn't generate a valid SQL query. Please try a different question.")

#######################################################################################
