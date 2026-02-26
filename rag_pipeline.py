import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from src.utils.simple_llm import SimpleLLM


# ----------------------------
# Build Vector Store
# ----------------------------
def build_vectorstore():

    # Absolute path fix
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(BASE_DIR, "data", "policies.txt")

    # Load policies
    loader = TextLoader(file_path)
    documents = loader.load()

    if not documents:
        raise ValueError("No documents loaded. Check policies.txt file.")

    # Split text into chunks
    splitter = CharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=20
    )
    docs = splitter.split_documents(documents)

    if not docs:
        raise ValueError("Document splitting failed. No chunks created.")

    # Create embeddings (LOCAL model, no API key)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Create FAISS vector store
    vectorstore = FAISS.from_documents(docs, embeddings)

    return vectorstore


# Build once when app starts
vectorstore = build_vectorstore()
llm = SimpleLLM()


# ----------------------------
# Manual RAG Logic
# ----------------------------
def get_answer(query):

    if not query.strip():
        return "Please enter a valid question."

    # Retrieve similar documents
    docs = vectorstore.similarity_search(query, k=2)

    if not docs:
        return "Sorry, I couldn't find relevant information."

    # Combine retrieved text
    context = "\n\n".join([doc.page_content for doc in docs])

    # Create prompt
    prompt = f"""
Use the following policy information to answer the question.

Policy:
{context}

Question:
{query}
"""

    # Generate response
    response = llm._call(prompt)

    return response