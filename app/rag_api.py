from fastapi import FastAPI, HTTPException
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain import hub

from app.settings import Settings
from app.models import QuestionRequest, QuestionResponse

settings = Settings()

# Inizialize FastAPI app
app = FastAPI(title="RAG API for Financial Docs")

# Prepare Qdrant vector store
client = QdrantClient(path=settings.qdrant_url)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=settings.openai_api_key)
vector_store = QdrantVectorStore(client=client, collection_name="fin-docs", embedding=embeddings)

# Declare LLM and prompt
llm = ChatOpenAI(model="gpt-4o-mini", api_key=settings.openai_api_key)
prompt = hub.pull("rlm/rag-prompt")

# Define the RAG endpoint
@app.post("/rag")
async def rag_query(rag_request: QuestionRequest):
    try:
        # Retruieve relevant documents
        docs_with_scores = vector_store.similarity_search_with_score(rag_request.question, k=5)
        if not docs_with_scores:
            raise ValueError("No relevant documents found.")

        # Prepare context
        context = "\n\n".join(doc.page_content for doc, _ in docs_with_scores)
        prompt_input = prompt.invoke({"question": rag_request.question, "context": context})

        # Generate answer
        answer = llm.invoke(prompt_input)
        return QuestionResponse(question=rag_request.question, answer=answer.content)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Run the app with: uvicorn app.rag_api:app --reload