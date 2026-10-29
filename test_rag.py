from core.document_loader import (
    load_document
)

from core.rag_service import (
    create_vectorstore,
    build_rag_context
)

from core.llm_service import (
    ask_rag_llm
)


DOCUMENT_PATH = (
    "documents/company_policy.txt"
)


# --------------------------------------------------
# Load document
# --------------------------------------------------

text = load_document(
    DOCUMENT_PATH
)

print(
    f"Loaded document: "
    f"{len(text)} characters"
)


# --------------------------------------------------
# Create vector database
# --------------------------------------------------

create_vectorstore(
    text,
    "company_policy.txt"
)

print(
    "Document successfully indexed."
)


# --------------------------------------------------
# Ask question
# --------------------------------------------------

question = (
    "How long do customers have "
    "to return a product?"
)


# --------------------------------------------------
# Retrieve context
# --------------------------------------------------

context = build_rag_context(
    question
)

print(
    "\nRetrieved Context:"
)

print(context)


# --------------------------------------------------
# Generate answer
# --------------------------------------------------

answer = ask_rag_llm(
    question,
    context
)


print(
    "\nInsightForge Answer:"
)

print(answer)