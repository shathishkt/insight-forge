import os

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI


load_dotenv()


def create_llm():
    """
    Create the OpenAI chat model.
    """

    api_key = os.getenv(
        "OPENAI_API_KEY"
    )

    if not api_key:

        raise ValueError(
            "OPENAI_API_KEY was not found "
            "in the .env file."
        )

    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )


def ask_llm(
    question,
    context
):
    """
    Ask the LLM using supplied context.
    """

    llm = create_llm()

    prompt = f"""
You are InsightForge, an AI-powered
Business Intelligence Assistant.

Answer the user's question using ONLY
the supplied context.

IMPORTANT RULES:

1. Do not invent facts.
2. Do not invent numerical values.
3. If the context does not contain enough
   information, say so clearly.
4. Separate factual findings from
   recommendations.
5. Keep the answer business-oriented.
6. When appropriate, provide actionable
   recommendations.

CONTEXT:

{context}

USER QUESTION:

{question}

Provide a concise but useful answer.
"""

    response = llm.invoke(
        prompt
    )

    return response.content


def ask_rag_llm(
    question,
    rag_context
):
    """
    Answer a question using retrieved
    RAG context.
    """

    llm = create_llm()

    prompt = f"""
You are InsightForge, an AI-powered
Business Intelligence Assistant.

You are answering a question using
retrieved company/business documents.

Use ONLY the information provided
in the retrieved context.

IMPORTANT:

- Do not invent information.
- Do not rely on your general knowledge
  when the retrieved documents do not
  support the answer.
- If the answer cannot be found,
  explicitly say that the available
  documents do not contain enough information.
- Mention the relevant document/source
  when useful.
- Keep the response concise and professional.

RETRIEVED DOCUMENT CONTEXT:

{rag_context}

USER QUESTION:

{question}

Answer the question.
"""

    response = llm.invoke(
        prompt
    )

    return response.content