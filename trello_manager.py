import re
import os
from dotenv import load_dotenv
import requests

load_dotenv()


class TrelloManager:
    BASE_URL = 'https://api.trello.com/1'

    def __init__(self):
        """
        Initialize the TrelloManager with API credentials and List ID from environment variables.
        """
        self.API_KEY = os.environ["ENV_API_KEY"]
        self.API_TOKEN = os.environ["ENV_API_TOKEN"]
        self.LIST_ID = os.environ["ENV_LIST_ID"]

    def build_url(self, endpoint, **kwargs):
        """
        Helper method to construct URLs for Trello API requests.
        
        Args:
            endpoint (str): The API endpoint to be appended to the base URL.
            **kwargs: Additional query parameters to be included in the URL.
        
        Returns:
            tuple: A tuple containing the constructed URL and the parameters dictionary.
        """
        url = f"{self.BASE_URL}/{endpoint}"
        params = {'key': self.API_KEY, 'token': self.API_TOKEN}
        if kwargs:
            # Update the parameters with any additional keyword arguments provided
            params.update(kwargs)
        return url, params

    def get_cards_in_list(self, list_id):
        """
        Get all cards in a specified Trello list.
        
        Args:
            list_id (str): The ID of the Trello list.
        
        Returns:
            list: A list of cards in the specified Trello list.
        """
        url, params = self.build_url(f"lists/{list_id}/cards")
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_attachments_on_card(self, card_id):
        """
        Get all attachments on a specified Trello card.
        
        Args:
            card_id (str): The ID of the Trello card.
        
        Returns:
            list: A list of attachments on the specified Trello card.
        """
        url, params = self.build_url(f"cards/{card_id}/attachments")
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def delete_attachment_from_card(self, card_id, attachment_id):
        """
        Delete an attachment from a specified Trello card.
        
        Args:
            card_id (str): The ID of the Trello card.
            attachment_id (str): The ID of the attachment to be deleted.
        
        Returns:
            None
        """
        url, params = self.build_url(f"cards/{card_id}/attachments/{attachment_id}")
        response = requests.delete(url, params=params)
        response.raise_for_status()

    def clean_card_name(self, card_name):
        """
        Clean and harmonize the name of a Trello card.
        
        Args:
            card_name (str): The original name of the Trello card.
        
        Returns:
            str: The cleaned card name.
        """
        match = re.search(r"\((.+?)\)", card_name)
        return match.group(1) if match else card_name  # Return original name if no match is found
    
    def update_card_name(self, card_id, new_name):
        """
        Update the name of a specified Trello card.
        
        Args:
            card_id (str): The ID of the Trello card.
            new_name (str): The new name for the Trello card.
        
        Returns:
            None
        """
        url, params = self.build_url(f"cards/{card_id}")
        params['name'] = new_name
        response = requests.put(url, params=params)
        response.raise_for_status()
    
    def update_card_description(self, card_id, description=""):
        """
        Update the description of a specified Trello card.
        
        Args:
            card_id (str): The ID of the Trello card.
            description (str, optional): The new description for the Trello card. Defaults to an empty string.
        
        Returns:
            None
        """
        url, params = self.build_url(f"cards/{card_id}")
        params['desc'] = description
        response = requests.put(url, params=params)
        response.raise_for_status()
