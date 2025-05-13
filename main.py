from trello_manager import TrelloManager
import os
from dotenv import load_dotenv
import requests
from datetime import datetime

load_dotenv()

trello_manager = TrelloManager()


def log_message(message):
    """Log to console and file for GitHub Actions."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] {message}"
    print(formatted)  # Visible in GitHub Actions logs
    with open("trello_automation.log", "a") as f:
        f.write(formatted + "\n")

def run_automation(): 
    # DELETING ATTACHMENTS FROM CARDS
    try:
        cards = trello_manager.get_cards_in_list(os.environ["ENV_LIST_ID"])
        for card in cards:
            try:
                attachments = trello_manager.get_attachments_on_card(card['id'])
                attachment_found = False
                for attachment in attachments:
                    if attachment['name'] == os.environ["ATTACHMENT_NAME_TO_DELETE"]:
                        trello_manager.delete_attachment_from_card(card['id'], attachment['id'])
                        attachment_found = True
                        log_message(f'Attachment "{attachment["name"]}" deleted from card "{card["name"]}".')
                        break
                if not attachment_found:
                    log_message(f'Card "{card["name"]}" does not possess the specified attachment.')
            except requests.exceptions.RequestException as e:
                log_message(f"Error occurred while retrieving attachments for card '{card['name']}': {e}")
    except requests.exceptions.RequestException as e:
        log_message(f"Error occurred while retrieving cards from list: {e}")

    # CLEANING AND HARMONIZING CARD NAMES
    try:
        cards = trello_manager.get_cards_in_list(os.environ["ENV_LIST_ID"])
        for card in cards:
            try:
                original_name = card['name']
                new_name = trello_manager.clean_card_name(original_name)
                if new_name != original_name:
                    trello_manager.update_card_name(card['id'], new_name)
                    log_message(f'Card name updated: "{original_name}" -> "{new_name}".')
                else:
                    log_message(f'Card name is already clean: "{original_name}".')
            except requests.exceptions.RequestException as e:
                log_message(f"Error occurred while updating card '{card['name']}': {e}")
    except requests.exceptions.RequestException as e:
        log_message(f"Error occurred while retrieving cards from list: {e}")

    # DELETING DESCRIPTION FROM CARDS
    try:
        cards = trello_manager.get_cards_in_list(os.environ["ENV_LIST_ID"])
        for card in cards:
            try:
                trello_manager.update_card_description(card['id'], description="")
                log_message(f'Description cleared for card "{card["name"]}".')
            except requests.exceptions.RequestException as e:
                log_message(f"Error occurred while clearing description for card '{card['name']}': {e}")
    except requests.exceptions.RequestException as e:
        log_message(f"Error occurred while retrieving cards from list: {e}")

