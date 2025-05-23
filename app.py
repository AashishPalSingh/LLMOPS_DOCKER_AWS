from dotenv import load_dotenv
import os
import boto3
import streamlit as st


from langchain_community.vectorstores import FAISS
from langchain_aws import BedrockEmbeddings

from QASystem.ingestion import data_ingestion, get_vector_store

from QASystem.retrievalandgeneration import get_llama2_llm, get_response_llm

load_dotenv(".env")
bedrock = boto3.client(service_name="bedrock-runtime")
bedrock_embeddings = BedrockEmbeddings(
    model_id=os.getenv("EMBEDDING_MODEL_ID"), client=bedrock
)


def main():
    st.set_page_config("QA with Doc")
    st.header("QA with Doc using langchain and AWSBedrock")

    user_question = st.text_input("Ask a question from the pdf files")

    with st.sidebar:
        st.title("update or create the vector store")
        if st.button("vectors update"):
            with st.spinner("processing..."):
                docs = data_ingestion()
                get_vector_store(docs)
                st.success("done")

        if st.button("llama model"):
            with st.spinner("processing..."):
                faiss_index = FAISS.load_local(
                    "faiss_index",
                    bedrock_embeddings,
                    allow_dangerous_deserialization=True,
                )
                llm = get_llama2_llm()

                st.write(get_response_llm(llm, faiss_index, user_question))
                st.success("Done")


if __name__ == "__main__":
    main()
