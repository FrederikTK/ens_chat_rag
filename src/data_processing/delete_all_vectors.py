import logging
import time
from src.rag_system.vector_store import VectorStore
from src.utils.operation_lock import OperationLock

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def delete_all_vectors():
    lock = OperationLock()
    if not lock.acquire("deleting"):
        logger.error("Another operation is in progress. Please try again later.")
        return

    try:
        vector_store = VectorStore()
        
        # Get initial count
        initial_stats = vector_store.get_index_stats()
        logger.info(f"Initial vector count: {initial_stats['total_vector_count']}")

        # Delete vectors
        vector_store.delete_all_vectors()
        
        # Wait a bit for the deletion to propagate
        time.sleep(5)

        # Verify deletion
        final_stats = vector_store.get_index_stats()
        logger.info(f"Final vector count: {final_stats['total_vector_count']}")

        if final_stats['total_vector_count'] == 0:
            logger.info("All vectors successfully deleted.")
        else:
            logger.warning(f"Deletion may not have been complete. {final_stats['total_vector_count']} vectors remaining.")
    finally:
        lock.release()

if __name__ == "__main__":
    delete_all_vectors()