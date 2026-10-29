import os

from dotenv import load_dotenv

from langchain_chroma import Chroma

from langchain_huggingface import (
    HuggingFaceEmbeddings
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_core.documents import Document


load_dotenv()


VECTORSTORE_PATH = "vectorstore"


def get_embeddings():
    """
    Create the embedding model.

    This model runs locally and does not require
    an OpenAI embedding API call.
    """

    embeddings = HuggingFaceEmbeddings(
        model_name=(
            "sentence-transformers/"
            "all-MiniLM-L6-v2"
        )
    )

    return embeddings


def create_vectorstore(
    text,
    source_name
):
    """
    Split document text into chunks and store
    embeddings in Chroma.
    """

    if not text or not text.strip():

        raise ValueError(
            "The document does not contain readable text."
        )


    # --------------------------------------------------
    # Create LangChain document
    # --------------------------------------------------

    document = Document(
        page_content=text,
        metadata={
            "source": source_name
        }
    )


    # --------------------------------------------------
    # Split document
    # --------------------------------------------------

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(
        [document]
    )


    # --------------------------------------------------
    # Create embeddings
    # --------------------------------------------------

    embeddings = get_embeddings()


    # --------------------------------------------------
    # Create / update Chroma
    # --------------------------------------------------

    vectorstore = Chroma(
        collection_name="insightforge_documents",
        embedding_function=embeddings,
        persist_directory=VECTORSTORE_PATH
    )


    # --------------------------------------------------
    # Add chunks
    # --------------------------------------------------

    vectorstore.add_documents(
        chunks
    )


    return vectorstore


def get_vectorstore():
    """
    Load the existing Chroma vector database.
    """

    embeddings = get_embeddings()

    vectorstore = Chroma(
        collection_name="insightforge_documents",
        embedding_function=embeddings,
        persist_directory=VECTORSTORE_PATH
    )

    return vectorstore


def search_documents(
    question,
    k=4
):
    """
    Search the vector database for relevant
    document chunks.
    """

    vectorstore = get_vectorstore()

    results = vectorstore.similarity_search(
        question,
        k=k
    )

    return results


def build_rag_context(
    question,
    k=4
):
    """
    Build context from retrieved documents.
    """

    results = search_documents(
        question,
        k=k
    )

    if not results:

        return (
            "No relevant documents were found."
        )


    context_parts = []

    for index, document in enumerate(
        results,
        start=1
    ):

        source = document.metadata.get(
            "source",
            "Unknown"
        )

        context_parts.append(
            f"""
Source {index}: {source}

{document.page_content}
"""
        )

    return "\n".join(
        context_parts
    )