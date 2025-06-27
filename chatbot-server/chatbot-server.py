from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import os
import google.auth
from google import genai
from google.genai.types import GenerateContentConfig, Tool, Retrieval, VertexRagStore
import time

# Google GenAI Client setup
PROJECT_ID = "expense-delight"
LOCATION = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")
credentials, project = google.auth.default()
client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION, credentials=credentials)

# RAG Retrieval Tool configuration
MODEL_ID = "gemini-2.5-flash"
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
chat = client.chats.create(
    model=MODEL_ID,
    config=GenerateContentConfig(
        system_instruction='If you find link in the source, please provide the link in the response.',
        temperature=0,
        tools=[rag_retrieval_tool]
    )
)

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

class ChatRequest(BaseModel):
    prompt: str
    stream: bool = False

class ChatResponse(BaseModel):
    response: str

# @app.post("/chat", response_model=ChatResponse)
# def chat_endpoint(request: ChatRequest):
#     """Synchronous chat endpoint returning the full response as JSON."""
#     try:
#         chat = client.chats.create(
#             model=MODEL_ID,
#             config=GenerateContentConfig(tools=[rag_retrieval_tool])
#         )
#         if request.stream:
#             raise HTTPException(status_code=400, detail="Use /chat/stream for streaming responses")
#         response = chat.send_message(request.prompt)
#         return ChatResponse(response=response.text)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
def chat_stream(request: ChatRequest):
    """Streaming chat endpoint yielding text chunks as plain text."""
    try:
        def generate():
            for chunk in chat.send_message_stream(request.prompt):
                yield chunk.text
        return StreamingResponse(generate(), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3333)
