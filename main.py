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

    # EXTRACTING NAMES AND POLICY NUMBERS to CLEAN AND HARMONIZE CARD NAMES
    try:
        cards = trello_manager.get_cards_in_list(os.environ["ENV_LIST_ID"])
        for card in cards:
            try:
                # Get full card details including description
                card_details = trello_manager.get_card_details(card['id'])
                original_name = card_details['name']
                description = card_details.get('desc', '')
                
                # Extract person name and policy number
                person_name, policy_number, should_process = trello_manager.extract_name_and_policy(original_name, description)
                
                if should_process and person_name:
                    # Update card name to person's name
                    trello_manager.update_card_name(card['id'], person_name)
                    log_message(f'Card name updated: "{original_name}" -> "{person_name}".')
                    
                    # Update custom field with policy number
                    trello_manager.update_card_custom_field(card['id'], os.environ["POLICY_NUMBER_CUSTOM_FIELD_ID"], policy_number)
                    log_message(f'Policy number "{policy_number}" set in custom field for card "{person_name}".')
                else:
                    log_message(f'Card "{original_name}" skipped - no valid name found in description.')
                
            except requests.exceptions.RequestException as e:
                log_message(f"Error occurred while processing card '{card['name']}': {e}")
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

if __name__ == "__main__":
    run_automation()
    log_message("Automation completed.")
