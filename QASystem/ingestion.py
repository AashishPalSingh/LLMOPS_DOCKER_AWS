from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_aws import BedrockEmbeddings

import os
from dotenv import load_dotenv

import boto3

load_dotenv(".env")
print(" Embedding model id: ", os.getenv("EMBEDDING_MODEL_ID"))
bedrock = boto3.client(service_name="bedrock-runtime")
bedrock_embeddings = BedrockEmbeddings(
    model_id=os.getenv("EMBEDDING_MODEL_ID"),
    client=bedrock,
)


def data_ingestion():
    loader = PyPDFDirectoryLoader("./data")
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=1000)
    text_splitter.split_documents(documents)

    docs = text_splitter.split_documents(documents)

    return docs


def get_vector_store(docs):
    vector_store_faiss = FAISS.from_documents(docs, bedrock_embeddings)
    vector_store_faiss.save_local("faiss_index")
    return vector_store_faiss


if __name__ == "__main__":
    docs = data_ingestion()
    get_vector_store(docs)
