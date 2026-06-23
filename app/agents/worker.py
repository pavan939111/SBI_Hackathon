"""
Background worker running the stateful LangGraph orchestrator loop.
"""
import asyncio
import logging
import signal
import sys
from app.agents.graph import build_graph
from app.services.queue_manager import QueueManager
from app.services.whatsapp import WhatsAppService

# Set up logging context
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("banksaathi.worker")

class BackgroundWorker:
    """
    Background worker loop that dequeues tasks from Redis and runs
    the LangGraph agent pipeline.
    """
    def __init__(self):
        self.queue_manager = QueueManager()
        self.wa_service = WhatsAppService()
        self.graph = build_graph()
        self.running = True

    def stop(self, *args):
        """Triggers graceful shutdown of the worker loop."""
        logger.info("Shutdown signal received. Stopping worker loop...")
        self.running = False

    async def start(self):
        """Starts the worker polling loop."""
        logger.info("BankSaathi Background Worker started. Listening for tasks...")
        
        while self.running:
            try:
                task = await self.queue_manager.dequeue_task(timeout=3)
                if not task:
                    # No tasks available, yield control to event loop
                    await asyncio.sleep(0.1)
                    continue

                logger.info(f"Retrieved task from queue: {task}")
                
                # Setup agent state based on webhook task
                phone_number = task.get("sender", "")
                text_body = task.get("body", "")
                
                initial_state = {
                    "customer_id": None,
                    "phone_number": phone_number,
                    "messages": [{"role": "user", "content": text_body}],
                    "dms_level": 0,
                    "intent": None,
                    "language": "en",
                    "risk_tier": 1,
                    "matched_schemes": [],
                    "form_prefilled": {},
                    "requires_officer": False,
                    "recovery_context": {}
                }
                
                # Execute LangGraph pipeline
                thread_id = f"thread_{phone_number}"
                config = {"configurable": {"thread_id": thread_id}}
                
                logger.info(f"Invoking agent state graph for thread: {thread_id}")
                final_state = await self.graph.ainvoke(initial_state, config)
                
                logger.info(f"Agent state graph finished execution. Final state: {final_state}")
                
                # Direct response to user (acting as final outbound WhatsApp delivery)
                # In real scenario, the graph nodes themselves or a notifier class sends the payload
                outbound_text = f"BankSaathi processed your request: {final_state.get('intent')}"
                await self.wa_service.send_whatsapp_message(phone_number, outbound_text)
                
            except Exception as e:
                logger.error(f"Error processing queue task: {e}", exc_info=True)
                await asyncio.sleep(2) # Backoff before retry

async def main():
    worker = BackgroundWorker()
    
    # Register termination signals
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, worker.stop)
        except NotImplementedError:
            # signal handler registration is not implemented in Windows asyncio loops
            pass

    await worker.start()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Worker stopped by user.")
        sys.exit(0)
EOF
