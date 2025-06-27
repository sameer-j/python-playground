# -*- coding: utf-8 -*-

# pip install --upgrade --quiet google-genai
# additional steps for creation of rag corpus need to be added
# ref: https://colab.research.google.com/github/GoogleCloudPlatform/generative-ai/blob/main/gemini/rag-engine/intro_rag_engine.ipynb#scrollTo=4669c5cdbb5a

import sys
import os
from google import genai
import google.auth
from vertexai import rag


PROJECT_ID = "expense-delight"

LOCATION = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1")

credentials, project = google.auth.default()

client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION, credentials=credentials)

from google.genai.types import (
    GenerateContentConfig,
    GenerateContentResponse,
    Retrieval,
    Tool,
    VertexRagStore
)


def print_grounding_data(response: GenerateContentResponse) -> None:
    """Prints Gemini response with grounding citations in Markdown format."""

    # display(Markdown(f"> {response}"))
    if not (response.candidates and response.candidates[0].grounding_metadata):
        print("Information not found in the provided knowledge base")
        print(response.text)
        return

    grounding_metadata = response.candidates[0].grounding_metadata
    markdown_parts = []

    # Citation indexes are in bytes
    ENCODING = "utf-8"
    text_bytes = response.text.encode(ENCODING)
    last_byte_index = 0

    # Check if grounding_metadata.grounding_supports is not None before iterating
    if grounding_metadata.grounding_supports is not None:
        for support in grounding_metadata.grounding_supports:
            markdown_parts.append(
                text_bytes[last_byte_index : support.segment.end_index].decode(ENCODING)
            )

            # Generate and append citation footnotes (e.g., "[1][2]")
            footnotes = "".join([f"[{i + 1}]" for i in support.grounding_chunk_indices])
            markdown_parts.append(f" {footnotes}")

            # Update index for the next segment
            last_byte_index = support.segment.end_index

    # Append any remaining text after the last citation
    if last_byte_index < len(text_bytes):
        markdown_parts.append(text_bytes[last_byte_index:].decode(ENCODING))

    markdown_parts.append("\n\n----\n## Grounding Sources\n")

    # Build Grounding Sources Section
    markdown_parts.append("### Grounding Chunks\n")
    if grounding_metadata.grounding_chunks: # Also check if grounding_metadata.grounding_chunks is not None
        for i, chunk in enumerate(grounding_metadata.grounding_chunks, start=1):
            context = chunk.web or chunk.retrieved_context
            if not context:
                continue

            uri = context.uri
            title = context.title or "Source"
            print("URI: ", uri)
            print("Title: ", title)
            print("Context: ", context)

            # Convert GCS URIs to public HTTPS URLs
            if uri and uri.startswith("gs://"):
                uri = uri.replace("gs://", "https://storage.googleapis.com/", 1).replace(
                    " ", "%20"
                )
            markdown_parts.append(f"{i}. [{title}]({uri})\n")

    # Add Search/Retrieval Queries
    if grounding_metadata.web_search_queries:
        markdown_parts.append(
            f"\n**Web Search Queries:** {grounding_metadata.web_search_queries}\n"
        )
        if grounding_metadata.search_entry_point:
            markdown_parts.append(
                f"\n**Search Entry Point:**\n{grounding_metadata.search_entry_point.rendered_content}\n"
            )
    elif grounding_metadata.retrieval_queries:
        markdown_parts.append(
            f"\n**Retrieval Queries:** {grounding_metadata.retrieval_queries}\n"
        )

    print("".join(markdown_parts))

MODEL_ID = "gemini-2.5-flash"  # @param {type: "string"}

# PROMPT = "How to apply a Coupon while depositing?"

# PROMPT1 = "What is MPL?"

# GENERATED_CORPUS_NAME = "projects/expense-delight/locations/us-central1/ragCorpora/2882303761517117440"
GENERATED_CORPUS_NAME = "projects/1052818262145/locations/us-central1/ragCorpora/6341068275337658368"

rag_retrieval_tool = Tool(
    retrieval=Retrieval(
        vertex_rag_store=VertexRagStore(
            rag_corpora=[GENERATED_CORPUS_NAME],
            similarity_top_k=5,
            vector_distance_threshold=0.5,
        )
    )
)

# RAG_TEXT="What is RAG and why it is helpful?"

# response = client.models.generate_content(
#     model=MODEL_ID,
#     contents=RAG_TEXT,
#     config=GenerateContentConfig(tools=[rag_retrieval_tool]),
# )


chat = client.chats.create(
    model=MODEL_ID,
    config=GenerateContentConfig(
        tools=[
            rag_retrieval_tool
        ]
    ),
)

# CHAT1 = "What is RAG?"
# CHAT_FOLLOWUP = "Why is it helpful?"
# CHAT_FOLLOWUP2 = "Tell me recipe for home made pizza."

# CHAT1 = "How to apply a Coupon while depositing?"
# CHAT_FOLLOWUP = "What is MPL?"

# print("## Prompt")
# print(f"> {CHAT1}")
# response = chat.send_message(CHAT1)
# print_grounding_data(response)

# print("---\n")

# print("## Follow-up Prompt")
# print(f"> {CHAT_FOLLOWUP}")
# response = chat.send_message(CHAT_FOLLOWUP)

# print("## Follow-up Prompt")
# print(f"> {CHAT_FOLLOWUP2}")
# response = chat.send_message(CHAT_FOLLOWUP2)

CHAT1 = "How to play Rummy?"
CHAT_FOLLOWUP = "What happens if I leave the table?"
CHAT_FOLLOWUP2 = "Tell me recipe for home made pizza."

print("## Prompt")
print(f"> {CHAT1}")
# response = chat.send_message(CHAT1)
# print_grounding_data(response)

for chunk in chat.send_message_stream(CHAT1):
    print(chunk.text)

# print("---\n")

# print("## Follow-up Prompt")
# print(f"> {CHAT_FOLLOWUP2}")
# response = chat.send_message(CHAT_FOLLOWUP2)
# print_grounding_data(response)