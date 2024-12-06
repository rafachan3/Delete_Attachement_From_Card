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

    # Function to get cards in a list
    def get_cards_in_list(self, list_id):
        url = f'{self.BASE_URL}/lists/{list_id}/cards'
        params = {'key': self.API_KEY, 'token': self.API_TOKEN}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    # Function to get attachments on a card
    def get_attachments_on_card(self, card_id):
        url = f'{self.BASE_URL}/cards/{card_id}/attachments'
        params = {'key': self.API_KEY, 'token': self.API_TOKEN}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    # Function to delete an attachment from a card
    def delete_attachment_from_card(self, card_id, attachment_id):
        url = f'{self.BASE_URL}/cards/{card_id}/attachments/{attachment_id}'
        params = {'key': self.API_KEY, 'token': self.API_TOKEN}
        response = requests.delete(url, params=params)
        response.raise_for_status()
        print(f'Deleted attachment {attachment_id} from card {card_id}')