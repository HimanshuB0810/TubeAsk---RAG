# TubeAsk — Video Intelligence System 

TubeAsk is a high-performance Retrieval-Augmented Generation (RAG) terminal designed to index and query YouTube video content in real-time. Built with a focus on speed and accuracy, it leverages Gemini 2.5 Flash and FAISS vector indexing to provide a seamless "chat-with-video" experience.



## 🚀 Overview
The system allows users to provide a YouTube URL or Video ID, fetches the English transcript, and creates a searchable vector database. Users can then query the video content using natural language to receive structured, concise, and technically grounded answers.

## 🛠️ Tech Stack
* **Frontend**: Streamlit with custom CSS for a terminal-style UI
* **LLM**: Google Gemini 2.5 Flash
* **Orchestration**: LangChain
* **Vector Store**: FAISS (Facebook AI Similarity Search)
* **Embeddings**: HuggingFace (`sentence-transformers/all-MiniLM-L6-v2`)
* **Transcript Fetching**: `youtube-transcript-api`

## 🏗️ Core Architecture
The RAG pipeline follows a structured flow to ensure contextually relevant responses:

1.  **URL Processing**: The system accepts full YouTube URLs and extracts the unique 11-character Video ID.
2.  **Transcript Extraction**: Fetches the full text transcript using the `YouTubeTranscriptApi`.
3.  **Text Splitting**: Uses `RecursiveCharacterTextSplitter` to break the transcript into 500-character chunks with a 100-character overlap.
4.  **Vectorization**: Chunks are converted into embeddings and stored in a FAISS index.
5.  **Retrieval**: Utilizes Maximal Marginal Relevance (MMR) search to fetch the top 2 most relevant context snippets.
6.  **Generation**: A custom `PromptTemplate` guides the LLM to generate structured Markdown responses based strictly on the retrieved context.



## 📂 Project Structure
* `app.py`: The main Streamlit application handling UI state, sidebar configuration, and chat interface.
* `rag_backend.py`: The logic layer responsible for transcript fetching, document processing, and LangChain orchestration.
* `static/style.css`: Custom terminal-themed styling providing a professional "Cyberpunk" aesthetic.

## 🔧 Installation & Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/himanshub0810/tubeask-rag.git
    cd tubeask-rag
    ```

2.  **Install dependencies**:
    ```bash
    pip install streamlit youtube-transcript-api langchain langchain-community langchain-huggingface langchain-google-genai python-dotenv faiss-cpu
    ```

3.  **Configure Environment Variables**:
    Create a `.env` file in the root directory and add your API keys:
    ```env
    GOOGLE_API_KEY=your_gemini_api_key_here
    HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here
    ```

4.  **Run the application**:
    ```bash
    streamlit run app.py
    ```

## 📝 Usage Guide
* **Initialize**: Enter a YouTube URL or Video ID in the sidebar and click **▶ LOAD & ANALYZE**.
* **Query**: Once indexed, use the chat terminal to ask questions like "What are the main topics?" or "Summarize the conclusion".
* **Response Format**: The system provides structured answers with an **Overview**, **Key Points**, and **Additional Details**.

## 🛡️ Error Handling
The system includes built-in exception handling for common transcript issues:
* **TranscriptsDisabled**: Notifies if captions are turned off for a video.
* **NoTranscriptFound**: Alerts if no English transcript is available.
* **Context Missing**: If the information isn't in the video, the system responds: *"I don't know based on the provided context."*