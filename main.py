from langchain.chains import LLMChain
from langchain.llms.bedrock import Bedrock
from langchain.prompts import PromptTemplate
import boto3
import os
import streamlit as st

os.environ["AWS_PROFILE"] = "william"

#bedrock client

bedrock_client = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-west-2"
)

modelID = "anthropic.claude-v2"
# modelID = "amazon.titan-tg1-large"


llm = Bedrock(
    model_id=modelID,
    client=bedrock_client,
    model_kwargs={"max_tokens_to_sample": 2000,"temperature":0.9}
)

def my_chatbot(language,freeform_text):
    prompt = PromptTemplate(
        input_variables=["language", "freeform_text"],
        template="You are a chatbot. You are in {language}. Your job is to give rating from 1 to 5 stars of text provided by Human. This text is coming from customers using our Fazz Agen App. If possible, also give your insight on what can be done better to improve our app. The Human will most likely use Bahasa, and you are required to respond in English. \n\n{freeform_text}"
    )

    bedrock_chain = LLMChain(llm=llm, prompt=prompt)

    response=bedrock_chain({'language':language, 'freeform_text':freeform_text})
    return response

st.title("Your Google Playstore Review Assistant")

language = st.sidebar.selectbox("Language", ["english", "bahasa indonesia"])

# uncomment for upload file button feature
# uploaded_file = st.file_uploader("Choose a file")
# if uploaded_file is not None:
#     # To read file as bytes:
#     bytes_data = uploaded_file.getvalue()
#     st.write(bytes_data)

#     # To convert to a string based IO:
#     stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
#     st.write(stringio)

#     # To read file as string:
#     string_data = stringio.read()
#     st.write(string_data)

#     # Can be used wherever a "file-like" object is accepted:
#     dataframe = pd.read_csv(uploaded_file)
#     st.write(dataframe)

if language:
    freeform_text = st.sidebar.text_area(label="what is your question?",
    max_chars=100000)

if freeform_text:
    response = my_chatbot(language,freeform_text)
    st.write(response['text'])