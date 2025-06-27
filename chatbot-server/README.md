# Chatbot Server

This project provides a simple chatbot server using FastAPI that leverages Google's Generative AI models with Retrieval-Augmented Generation (RAG).

## Features

-   **FastAPI Backend**: A high-performance Python web framework.
-   **Google Generative AI**: Utilizes the Gemini family of models.
-   **Retrieval-Augmented Generation (RAG)**: Connects the model to a Vertex AI RAG corpus for more grounded and knowledgeable responses.
-   **Streaming API**: Provides a real-time, streaming response for chat interactions.

## Prerequisites

-   Python 3.8+
-   A Google Cloud Project with the Vertex AI API enabled.
-   A configured RAG Corpus in Vertex AI.
-   The `gcloud` CLI installed and authenticated.

## Setup and Installation

1.  **Clone the repository (or download the files):**
    ```bash
    git clone <your-repo-url>
    cd chatbot-server
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Authenticate with Google Cloud:**
    Log in with your user credentials. This command will store your application default credentials.
    ```bash
    gcloud auth application-default login
    ```
    Set your project ID.
    ```bash
    gcloud config set project YOUR_PROJECT_ID
    ```

## Configuration

The server is configured through the constants at the top of `chatbot-server.py`.

-   `PROJECT_ID`: Your Google Cloud Project ID.
-   `LOCATION`: The Google Cloud region for your resources (defaults to `us-central1`).
-   `MODEL_ID`: The Gemini model to use (e.g., `gemini-1.5-flash`).
-   `GENERATED_CORPUS_NAME`: The full resource name of your RAG corpus in Vertex AI.

Make sure to update these values to match your GCP setup.

## Usage

Run the server with Uvicorn:

```bash


```

The server will be available at `http://localhost:8000`.

### API Endpoint

The server exposes a single streaming endpoint:

-   `POST /chat`

You can interact with it using `curl` or any API client.

**Example `curl` command:**

```bash
curl -X POST http://localhost:8000/chat \
-H "Content-Type: application/json" \
-d '{"prompt": "How do I play Rummy?"}' \
--no-buffer
```
The `--no-buffer` flag is important to see the streaming response as it arrives.

## Note on Concurrency

The current implementation initializes the `chat` object globally when the application starts. This is efficient as it avoids creating a new chat session for every request. However, it also means that **all concurrent users will share the same chat session and history**. For a simple demonstration or a single-user application, this is acceptable. For a multi-user production environment, you would need to manage chat sessions on a per-user basis (e.g., using a session ID and storing chat objects in a dictionary). 