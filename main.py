from trello_manager import TrelloManager
import os
from dotenv import load_dotenv
import requests

load_dotenv()

trello_manager = TrelloManager()

try:
    # Get all cards in the target list
    cards = trello_manager.get_cards_in_list(os.environ["ENV_LIST_ID"])
    
    # Iterate through each card
    for card in cards:
        try:
            # Get attachments on the card
            attachments = trello_manager.get_attachments_on_card(card['id'])
            
            # Find the attachment to delete by name
            attachment_found = False
            for attachment in attachments:
                if attachment['name'] == os.environ["ATTACHMENT_NAME_TO_DELETE"]:
                    # Delete the attachment
                    trello_manager.delete_attachment_from_card(card['id'], attachment['id'])
                    attachment_found = True
                    print(f'Attachment "{attachment["name"]}" deleted from card "{card["name"]}".')
                    break  # Stop searching after deleting
            
            # If no matching attachment is found, print a message
            if not attachment_found:
                print(f'Card "{card["name"]}" does not possess the specified attachment.')

        except requests.exceptions.RequestException as e:
            print(f"Error occurred while retrieving attachments for card '{card['name']}': {e}")

except requests.exceptions.RequestException as e:
    print(f"Error occurred while retrieving cards from list: {e}")