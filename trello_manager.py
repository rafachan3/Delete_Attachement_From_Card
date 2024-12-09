import re
import os
from dotenv import load_dotenv
import requests

load_dotenv()


class TrelloManager:
    BASE_URL = 'https://api.trello.com/1'

    def __init__(self):
        # Load API credentials and List ID from environment variables
        self.API_KEY = os.environ["ENV_API_KEY"]
        self.API_TOKEN = os.environ["ENV_API_TOKEN"]
        self.LIST_ID = os.environ["ENV_LIST_ID"]

    # Helper method to construct URLs
    def build_url(self, endpoint, **kwargs):
        url = f"{self.BASE_URL}/{endpoint}"
        params = {'key': self.API_KEY, 'token': self.API_TOKEN}
        if kwargs:
            # Update the parameters with any additional keyword arguments provided
            params.update(kwargs)
        return url, params

    # Function to get cards in a list
    def get_cards_in_list(self, list_id):
        url, params = self.build_url(f"lists/{list_id}/cards")
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    # Function to get attachments on a card
    def get_attachments_on_card(self, card_id):
        url, params = self.build_url(f"cards/{card_id}/attachments")
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    # Function to delete an attachment from a card
    def delete_attachment_from_card(self, card_id, attachment_id):
        url, params = self.build_url(f"cards/{card_id}/attachments/{attachment_id}")
        response = requests.delete(url, params=params)
        response.raise_for_status()

    # Function to clean and harmonize card names
    def clean_card_name(self, card_name):
        # Define the regex pattern to extract <name>
        match = re.search(r"\((.+?)\)", card_name)
        return match.group(1) if match else card_name  # Return original name if no match is found
    
    # Function to update the name of a card
    def update_card_name(self, card_id, new_name):
        url, params = self.build_url(f"cards/{card_id}")
        params['name'] = new_name
        response = requests.put(url, params=params)
        response.raise_for_status()
    
        # Function to update the description of a card
    def update_card_description(self, card_id, description=""):
        """
        Updates the description of a card.
        By default, it clears the description.
        """
        url, params = self.build_url(f"cards/{card_id}")
        params['desc'] = description
        response = requests.put(url, params=params)
        response.raise_for_status()
