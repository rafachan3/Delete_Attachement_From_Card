from trello_manager import TrelloManager
import os
from dotenv import load_dotenv

load_dotenv()

# Create an instance of TrelloManager
trello_manager = TrelloManager()

# Get all cards in the target list
cards = trello_manager.get_cards_in_list(os.environ["ENV_LIST_ID"])
    
# Iterate through each card
for card in cards:
    # Get attachments on the card
    attachments = trello_manager.get_attachments_on_card(card['id'])
        
    # Find the attachment to delete by name
    for attachment in attachments:
        if attachment['name'] == os.environ["ATTACHMENT_NAME_TO_DELETE"]:
            # Delete the attachment
            trello_manager.delete_attachment_from_card(card['id'], attachment['id']) 