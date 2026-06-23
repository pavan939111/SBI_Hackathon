"""
Queue Manager Service for Enqueuing Webhook Payload tasks to Redis.
"""
import json
import logging
from typing import Optional, Dict, Any
from app.db.redis_client import redis_client

logger = logging.getLogger(__name__)

class QueueManager:
    """
    Handles task buffering on Redis queues to separate FastAPI requests from
    heavy background agent processing.
    """
    def __init__(self, queue_name: str = "banksaathi_tasks"):
        self.queue_name = queue_name

    async def enqueue_task(self, payload: Dict[str, Any]) -> bool:
        """Pushes a payload dictionary to the back of the Redis list queue."""
        try:
            serialized = json.dumps(payload)
            await redis_client.rpush(self.queue_name, serialized)
            logger.info(f"Successfully enqueued task in '{self.queue_name}'")
            return True
        except Exception as e:
            logger.error(f"Failed to enqueue task in '{self.queue_name}': {e}")
            return False

    async def dequeue_task(self, timeout: int = 5) -> Optional[Dict[str, Any]]:
        """Blocks up to timeout seconds until a task is available to pop from the queue."""
        try:
            # blpop returns a tuple: (queue_name, popped_value)
            result = await redis_client.blpop(self.queue_name, timeout=timeout)
            if result:
                _, serialized = result
                return json.loads(serialized)
            return None
        except Exception as e:
            logger.error(f"Error popping task from Redis queue '{self.queue_name}': {e}")
            return None
