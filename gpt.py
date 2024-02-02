from langchain.chains import LLMChain
from langchain.llms.bedrock import Bedrock
from langchain.prompts import PromptTemplate
import boto3
import os
import streamlit as st
import time

# Setup environment and bedrock client
os.environ["AWS_PROFILE"] = "william"
bedrock_client = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-west-2"
)

modelID = "anthropic.claude-v2"

llm = Bedrock(
    model_id=modelID,
    client=bedrock_client,
    model_kwargs={"max_tokens_to_sample": 2000, "temperature": 0.9}
)

def chat_with_ai(freeform_text):
    prompt = PromptTemplate(
        input_variables=["language", "freeform_text"],
        template="You are a chatbot. You are in english. The general sentiment for this review is: The reviews indicate that overall, users find the Payfazz app very useful and convenient for transactions like phone credit top-up, bill payments and money transfers. Many praise the app for its user-friendly interface, attractive promotions, economical rates and good customer support. However, some users faced technical issues like failed transactions, problems with refunds and account access. There are requests for new features like game vouchers, QR payments and electricity token top-up. While users are largely positive, the feedback indicates there is room for improvement in reliability, adding more payment options and faster issue resolution. Addressing these concerns can help enhance users' experience. The Human will most likely ask you about this so you need to be prepared to answer. \n\n{freeform_text}"
    )
    bedrock_chain = LLMChain(llm=llm, prompt=prompt)
    response = bedrock_chain({'language': "English", 'freeform_text': freeform_text})
    return response

def app():
    st.title("Your Google Playstore Review Assistant")

    # Initialize session state variables if not already present
    if 'upload_completed' not in st.session_state:
        st.session_state.upload_completed = False
    if 'report_downloaded' not in st.session_state:
        st.session_state.report_downloaded = False

    # File upload section
    if not st.session_state.upload_completed:
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file is not None:
            # Simulate file processing delay
            with st.spinner('Processing the file...'):
                time.sleep(15)  # Simulate a delay, e.g., 5 seconds
            st.session_state.upload_completed = True
            st.success("File successfully uploaded.")

    # Show the report download button only if the file has been uploaded
    if st.session_state.upload_completed and not st.session_state.report_downloaded:
        report_link = r"C:\Users\William\Desktop\Mar 2023 - Fazz Agen Review.xlsx"
        if st.download_button(label="Download Report",
                              data=open(report_link, "rb"),
                              file_name="processed_report.xlsx",
                              mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"):
            st.session_state.report_downloaded = True  # Simulate the report being downloaded

    # AI Chatbot interaction is available only after the report download button is interacted with
    if st.session_state.report_downloaded:
        st.header("Discuss Your Report with Our AI")
        user_question = st.text_input("Ask me anything about your report:")
        if user_question:
            response = chat_with_ai(user_question)
            st.text_area("Assistant:", value=response['text'], height=1000, disabled=True)

if __name__ == "__main__":
    app()
