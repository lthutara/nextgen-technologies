import uvicorn
from app.api.main import app
from app.scheduler import ArticleScheduler
import signal
import sys

scheduler = ArticleScheduler()

def signal_handler(sig, frame):
    print("Shutting down gracefully...")
    scheduler.stop()
    sys.exit(0)

if __name__ == "__main__":
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start the scheduler
    scheduler.start()
    
    # Run the FastAPI app
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")