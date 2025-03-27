import logging
from fastapi import FastAPI, HTTPException, Depends
from models import Game, Player, BetRequest, FoldRequest, GameStatusResponse
from init import app  # Import the FastAPI app from init.py

# Initialize game instance
game = Game()

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# API to join the game
@app.post("/join")
async def join_game(player_name: str):
    if any(player.name == player_name for player in game.players):
        raise HTTPException(status_code=400, detail="Player already in game.")
    
    new_player = Player(name=player_name)
    game.players.append(new_player)
    logging.info(f"Player {player_name} joined the game.")
    return {"message": f"Player {player_name} has joined."}

# API to place a bet
@app.post("/bet")
async def place_bet(request: BetRequest):
    player = next((p for p in game.players if p.name == request.name and p.is_active), None)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found or inactive.")
    
    success, error = player.place_bet(request.amount)
    if not success:
        raise HTTPException(status_code=400, detail=error)
    
    game.pot += request.amount
    logging.info(f"Player {request.name} bet {request.amount}. Current pot: {game.pot}")
    return {"message": f"Bet of {request.amount} placed by {request.name}", "pot": game.pot}

# API to fold
@app.post("/fold")
async def fold(request: FoldRequest):
    player = next((p for p in game.players if p.name == request.name and p.is_active), None)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found or already folded.")

    player.fold()
    logging.info(f"Player {request.name} folded.")
    return {"message": f"Player {request.name} has folded."}

# API to check game status
@app.get("/status", response_model=GameStatusResponse)
async def get_game_status():
    current_player = game.current_turn_order[game.current_turn_index] if game.current_turn_order else None
    return {
        "is_active": game.is_active,
        "pot": game.pot,
        "current_turn": current_player,
        "players": [{"name": p.name, "balance": p.balance, "active": p.is_active} for p in game.players]
    }

# API to show current pot
@app.get("/show_pot")
async def show_pot():
    return {"pot": game.pot}

if __name__ == "__main__":
    from init import start_player_api
    start_player_api()
