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
        