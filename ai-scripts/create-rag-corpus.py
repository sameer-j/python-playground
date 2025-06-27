import os
from google import genai
import google.auth
from vertexai import rag


PROJECT_ID = "expense-delight"

LOCATION = os.environ.get("GOOGLE_CLOUD_REGION", "global")

RAG_CORPUS_DISPLAYNAME = "faq-jsonl-rag-corpus-new"

FILE_PATH = "/Users/sameer/personal/projects/python-playground/util-scripts/latest.jsonl"


RAG_TEXT="How to apply a Coupon while depositing?"

credentials, project = google.auth.default()

client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION, credentials=credentials)

from google.genai.types import (
    GenerateContentConfig,
    GenerateContentResponse,
    Retrieval,
    Tool,
    VertexRagStore
)

EMBEDDING_MODEL = "publishers/google/models/text-embedding-005"  # @param {type:"string", isTemplate: true}

# rag_corpus = rag.create_corpus(
#     display_name=RAG_CORPUS_DISPLAYNAME,
#     backend_config=rag.RagVectorDbConfig(
#         rag_embedding_model_config=rag.RagEmbeddingModelConfig(
#             vertex_prediction_endpoint=rag.VertexPredictionEndpoint(
#                 publisher_model=EMBEDDING_MODEL
#             )
#         )
#     ),
# )


# print(rag.list_corpora()) # to check if the corpus is created

# GENERATED_CORPUS_NAME = rag_corpus.name

# GENERATED_CORPUS_NAME = "projects/expense-delight/locations/us-central1/ragCorpora/2882303761517117440"

GENERATED_CORPUS_NAME = "projects/1052818262145/locations/us-central1/ragCorpora/6341068275337658368"

print("GENERATED_CORPUS_NAME: ", GENERATED_CORPUS_NAME)

# rag_file = rag.upload_file(
#     corpus_name=GENERATED_CORPUS_NAME,
#     path=FILE_PATH,
#     display_name="FAQ KB Complete",
#     description="FAQ KB Complete",
# )

INPUT_GCS_BUCKET = (
    "gs://rinku-mpl/ai-faq-chatbot/latest_jsonl_new/"
)

response = rag.import_files(
    corpus_name=GENERATED_CORPUS_NAME,
    paths=[INPUT_GCS_BUCKET],
    # Optional
    transformation_config=rag.TransformationConfig(
        chunking_config=rag.ChunkingConfig(chunk_size=1024, chunk_overlap=100)
    ),
    max_embedding_requests_per_min=900,  # Optional
)
print(response)

# Direct context retrieval
# response = rag.retrieval_query(
#     rag_resources=[
#         rag.RagResource(
#             rag_corpus=GENERATED_CORPUS_NAME,
#             # Optional: supply IDs from `rag.list_files()`.
#             # rag_file_ids=["rag-file-1", "rag-file-2", ...],
#         )
#     ],
#     rag_retrieval_config=rag.RagRetrievalConfig(
#         top_k=10,  # Optional
#         filter=rag.Filter(
#             vector_distance_threshold=0.5,  # Optional
#         ),
#     ),
#     text=RAG_TEXT,
# )
# print(response)
