import uvicorn
from app.api.main import app

if __name__ == "__main__":
    # Run the FastAPI app, which now manages the scheduler lifecycle.
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
