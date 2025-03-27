import logging
import uvicorn
from fastapi import FastAPI

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Constants
PLAYER_NAME = "Player1"
PLAYER_API_URL = "http://127.0.0.1:8001"
DEALER_API_URL = "http://127.0.0.1:8000"

# Initialize FastAPI app
app = FastAPI()

# Health Check Endpoint
@app.get("/ping")
async def ping():
    return {"message": "pong"}

def start_player_api():
    """
    Starts the Player API server using uvicorn.
    Ensures logging is initialized before running the server.
    """
    logging.info(f"Starting Player API for {PLAYER_NAME} at {PLAYER_API_URL}")
    uvicorn.run(app, host="127.0.0.1", port=8001)

# Ensure this only runs when the script is executed directly
if __name__ == "__main__":
    start_player_api()
