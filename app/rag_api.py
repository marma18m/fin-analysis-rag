import logging

from fastapi import FastAPI, HTTPException
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain import hub

from app.settings import Settings
from app.models import QuestionRequest, QuestionResponse

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

settings = Settings()

# Initialize FastAPI app
app = FastAPI(title="RAG API for Financial Docs")

# Prepare Qdrant vector store
client = QdrantClient(settings.qdrant_url)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=settings.openai_api_key)
vector_store = QdrantVectorStore(client=client, collection_name="fin-docs", embedding=embeddings)

# Declare LLM and prompt
llm = ChatOpenAI(model="gpt-4o-mini", api_key=settings.openai_api_key)
prompt = hub.pull("rlm/rag-prompt")

# Define the RAG endpoint
@app.post("/rag")
async def rag_query(rag_request: QuestionRequest):
    try:
        logger.info(f"Received question: {rag_request.question}")
        # Retruieve relevant documents
        docs_with_scores = vector_store.similarity_search_with_score(rag_request.question, k=5)
        logger.info(f"Retrieved {len(docs_with_scores)} documents from vector store")
        if not docs_with_scores:
            logger.warning("No relevant documents found.")
            raise ValueError("No relevant documents found.")

        # Prepare context
        context = "\n\n".join(doc.page_content for doc, _ in docs_with_scores)
        prompt_input = prompt.invoke({"question": rag_request.question, "context": context})

        # Generate answer
        answer = llm.invoke(prompt_input)
        logger.info("Successfully generated answer.")
        return QuestionResponse(question=rag_request.question, answer=answer.content)

    except Exception as e:
        logger.error(f"RAG query failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
    
# Run the app with: uvicorn app.rag_api:app --reload