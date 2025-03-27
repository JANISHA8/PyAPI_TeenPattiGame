from pydantic import BaseModel
from typing import List, Optional

# Card Model
class Card(BaseModel):
    rank: str
    suit: str
    name: str

# Player Model
class Player:
    def __init__(self, name: str, balance: float = 100.0):
        self.name = name
        self.balance = balance
        self.cards = []
        self.current_bet = 0.0
        self.is_active = True

    def place_bet(self, amount: float):
        if amount > self.balance:
            return False, "Insufficient balance."
        self.balance -= amount
        self.current_bet += amount
        return True, None

    def fold(self):
        self.is_active = False

# Game Model
class Game:
    def __init__(self):
        self.players = []
        self.is_active = False
        self.current_turn_order = []
        self.current_turn_index = 0
        self.pot = 0.0
        self.deck = []

# API Models
class JoinGameRequest(BaseModel):
    name: str
    host_url: str

class BetRequest(BaseModel):
    name: str
    amount: float

class FoldRequest(BaseModel):
    name: str

class GameStatusResponse(BaseModel):
    is_active: bool
    pot: float
    current_turn: Optional[str]
    players: List[dict]

class EndGameResponse(BaseModel):
    message: str






















# _init_.py for Teen Patti Game Package

from pydantic import BaseModel
from typing import List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Card Model
class Card(BaseModel):
    rank: str
    suit: str
    name: str

# Player Model
class Player:
    def _init_(self, name: str, balance: float = 100.0):
        self.name = name
        self.balance = balance
        self.cards: List[Card] = []  # Holds the player's cards
        self.current_bet = 0.0
        self.is_active = True

    def place_bet(self, amount: float):
        if amount > self.balance:
            return False, "Insufficient balance."
        self.balance -= amount
        self.current_bet += amount
        return True, None

    def fold(self):
        self.is_active = False

# Game Model
class Game:
    def _init_(self):
        self.players: List[Player] = []  # Holds all players in the game
        self.is_active = False
        self.current_turn_order: List[str] = []  # Turn order based on player names
        self.current_turn_index = 0
        self.pot = 0.0  # Total bets in the game pot
        self.deck: List[Card] = []  # Represents the deck of cards

    def add_player(self, player: Player):
        """Adds a new player to the game."""
        self.players.append(player)
        logging.info(f"Player {player.name} added to the game.")

    def start_game(self):
        """Starts the game and shuffles the deck."""
        if len(self.players) < 2:
            logging.warning("Not enough players to start the game.")
            return False
        self.is_active = True
        self.deck = self.shuffle_deck()
        logging.info("Game has started!")
        return True

    def shuffle_deck(self):
        """Generates and shuffles the deck."""
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        deck = [Card(rank=rank, suit=suit, name=f"{rank} of {suit}") for suit in suits for rank in ranks]
        from random import shuffle
        shuffle(deck)
        return deck

# API Models
class JoinGameRequest(BaseModel):
    name: str
    host_url: str

class BetRequest(BaseModel):
    name: str
    amount: float

class FoldRequest(BaseModel):
    name: str

class GameStatusResponse(BaseModel):
    is_active: bool
    pot: float
    current_turn: Optional[str]
    players: List[dict]

class EndGameResponse(BaseModel):
    message: str

# Initialize Game Instance
game_instance = Game()

# Log package initialization
logging.info("Teen Patti Game Package initialized!")