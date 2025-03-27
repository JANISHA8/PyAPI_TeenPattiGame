from pydantic import BaseModel
from typing import List, Optional
import logging
import random

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define suits and values for card generation
SUITS = ['H', 'D', 'C', 'S']  # Hearts, Diamonds, Clubs, Spades
VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# Card Model
class Card(BaseModel):
    rank: str
    suit: str

    @property
    def name(self):
        return f"{self.rank}{self.suit}"

# Player Model
class Player:
    def __init__(self, name: str, balance: float = 100.0):
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

    def receive_cards(self, cards: List[Card]):
        self.cards = cards

# Game Model
class Game:
    def __init__(self):
        self.players: List[Player] = []  # Holds all players in the game
        self.is_active = False
        self.current_turn_order: List[str] = []  # Turn order based on player names
        self.current_turn_index = 0
        self.pot = 0.0  # Total bets in the game pot
        self.deck: List[Card] = self.generate_deck()  # Initializes a shuffled deck

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
        self.shuffle_deck()
        for player in self.players:
            player.is_active = True
            player.current_bet = 0.0
        logging.info("Game has started!")
        return True

    def generate_deck(self) -> List[Card]:
        """Generates a full deck of 52 cards."""
        return [Card(rank=value, suit=suit) for suit in SUITS for value in VALUES]

    def shuffle_deck(self):
        """Shuffles the deck."""
        random.shuffle(self.deck)

    def deal_cards(self, num_cards: int = 3):
        """Deals `num_cards` to each player."""
        if len(self.deck) < num_cards * len(self.players):
            logging.error("Not enough cards in deck to deal.")
            return False
        for player in self.players:
            player.receive_cards([self.deck.pop() for _ in range(num_cards)])
        return True

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
