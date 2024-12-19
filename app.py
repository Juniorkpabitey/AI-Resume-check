from dotenv import load_dotenv
load_dotenv()
import streamlit as st 
import os
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai 

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,pdf_content[0],prompt])
    
    return response.text()

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ##Convert the pdf to image
        images=pdf2image.convert_from_bytes(uploaded_file.read())
    
        first_page=images[0]
    
        #Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
    
        pdf_parts = [
                {
            "mime_type": "image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode()
                }
            ]
    
        return pdf_parts
    else:
        raise FileNotFoundError("no file uploaded")
    

## Streamlit App Interface
st.set_page_config(page_title="AI Resume Checker")
st.header("AI Resume Requirement Check")
input_text=st.text_area("Job Description", key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("File uploaded Successfully")
    
submit1= st.button("Tell me about the resume")

submit2=st.button("How can i improve my skills")

submit3=st.button("Percentage match")

input_prompt1 = """
    You are an experienced HR with Tech experience in the field of Data science or Full Stack web development or Big Data Engineering or
    DevOps or Data Analyst or machine learning or software Engineering. Your task is to review the 
    provided resume against the job description.
    Please share your professional evaluation on whether the candidate's profile aligns with the job description. 
    And also highlight the strengths and weakness of the applicant in relation to the job desciption and the resume
"""
input_prompt2 = """
    You are a Technincal Human resouce manager with expertise ecerything about Data science or Full Stack web development or Big Data Engineering or
    DevOps or Data Analyst or machine learning or software Engineering . Your role is to scrutinze the resume
    in light of the job description. Please provide a detailed analysis of the resume in relation to the job description.
    Share yoour insights on the candidate's profile and how it aligns with the job description. Additionally, opffer advice on enhancing the candidate's skills
"""
input_prompt3 = """
    Your are a skilled ATS(Application tracking System) scnanner with a deep understanding of Data science or Full Stack web development or Big Data Engineering or
    DevOps or Data Analyst or machine learning or software Engineering and ATS functionality.Your role is to scrutinze the resume
    in light of the job description. Please provide a detailed analysis of the resume in relation to the job description.
    Share your insights on the candidate's profile and how it aligns with the job description. Additionally, opffer advice on enhancing the candidate's skills

"""
if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_text,pdf_content,input_prompt1)
        st.subheader("Resume Evalation")
        st.write(response) 
    else:
        st.write("Please upload a file") 
        
elif submit3:
        if uploaded_file is not None:
            pdf_content=input_pdf_setup(uploaded_file)
            response=get_gemini_response(input_text,pdf_content,input_prompt3)
            st.subheader("Resume Evalation")
            st.write(response) 
        else:
            st.write("Please upload a file")