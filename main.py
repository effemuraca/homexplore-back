import uvicorn
from dotenv import load_dotenv
from app import app

if __name__ == "__main__":
    load_dotenv()
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True, timeout_keep_alive=3600)