import logging
from dotenv import load_dotenv
from app import app
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    load_dotenv()
    logger.info("Starting the FastAPI application.")
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True, timeout_keep_alive=3600)
