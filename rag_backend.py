
import os
from dotenv import load_dotenv

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def get_transcript(video_id: str) -> str:
    transcript_obj = YouTubeTranscriptApi().fetch(video_id)
    return " ".join(snippet.text for snippet in transcript_obj)

def build_chain(video_id: str):
    transcript = get_transcript(video_id)

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.create_documents([transcript])

    embedding = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    vector_store = FAISS.from_documents(chunks, embedding)
        
    retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 2})
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)

    prompt = PromptTemplate(
        template="""You are a technical assistant.

                    Generate a clean, structured, and concise answer based only on the provided context.

                    Rules:
                    - Use Markdown formatting
                    - Be concise and precise
                    - Use headings and bullet points
                    - Avoid repetition and filler text
                    - Do NOT include phrases like "based on the context" or "this document explains"

                    Structure the answer dynamically based on the question.

                    Use this format:

                    ## Overview
                    <Direct answer / summary>

                    ## Key Points
                    - Point 1
                    - Point 2
                    - Point 3

                    ## Additional Details (if applicable)
                    - Examples / explanation / steps (only if needed)

                    If the answer is not explicitly present in the context, respond:
                    "I don't know based on the provided context."

                    Context:
                    {context}

                    Question:
                    {question}


                    Answer:""",  
                            input_variables=["context", "question"]
                        )
    
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    parallel_chain = RunnableParallel({
        "context":retriever | RunnableLambda(format_docs),
        "question":RunnablePassthrough()
    }) 

    parser = StrOutputParser()

    final_chain = parallel_chain | prompt | llm | parser

    return final_chain

if __name__=="__main__":
    video_id = "osKyvYJ3PRM"
    question = "What is LLM?"
    final_chain = build_chain(video_id)
    result = final_chain.invoke(question) 

    print(result)