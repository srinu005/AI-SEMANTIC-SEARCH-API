from celery import Celery
import asyncio
from app.services.ai_engine import AIEngine
from qdrant_client import QdrantClient

celery_app = Celery('worker', broker='redis://redis:6379/0')
ai = AIEngine()
# Qdrant sync client for the worker
q_client = QdrantClient(host="qdrant", port=6333)

@celery_app.task(name="index_batch_task")
def index_batch_task(docs: list[dict]):
    """
    Satisfies: 'Process 500+ document queries concurrently'
    """
    loop = asyncio.get_event_loop()
    
    # Generate embeddings for the whole batch concurrently
    async def process_batch():
        tasks = [ai.get_embedding(d['content']) for d in docs]
        return await asyncio.gather(*tasks)

    vectors = loop.run_until_complete(process_batch())

    # Bulk upload to Qdrant
    q_client.upload_collection(
        collection_name="b2b_documents",
        vectors=vectors,
        payload=docs,
        ids=None # Auto-generate
    )
    return f"Indexed {len(docs)} documents"