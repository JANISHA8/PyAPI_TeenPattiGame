import requests
import logging

current_player_name = "Alice"
action = "bet"
amount = 10

try:
    if action == "bet":
        response = requests.post("http://127.0.0.1:8000/bet", json={"name": current_player_name, "amount": amount})
        logging.info(f"Bet Response: {response.status_code} - {response.json()}")

    elif action == "fold":
        response = requests.post("http://127.0.0.1:8000/fold", json={"name": current_player_name})
        logging.info(f"Fold Response: {response.status_code} - {response.json()}")

    elif action == "show":
        if len(active_players) == 2:
            response = requests.post("http://127.0.0.1:8000/compare_cards")
            logging.info(f"Compare Cards Response: {response.status_code} - {response.json()}")
        
        response = requests.post("http://127.0.0.1:8000/fold", json={"name": current_player_name})
        logging.info(f"Final Fold Response: {response.status_code} - {response.json()}")

except Exception as e:
    logging.error(f"Error contacting {current_player_name}: {e}")
