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

    def update_card_custom_field(self, card_id, field_id, value):
        """
        Update a custom field value on a specified Trello card.
        
        Args:
            card_id (str): The ID of the Trello card.
            field_id (str): The ID of the custom field.
            value (str): The new value for the custom field.
        
        Returns:
            None
        """
        url, params = self.build_url(f"cards/{card_id}/customField/{field_id}/item")
        data = {'value': {'text': value}}
        response = requests.put(url, params=params, json=data)
        response.raise_for_status()

    def get_card_details(self, card_id):
        """
        Get detailed information about a specific Trello card including description.
        
        Args:
            card_id (str): The ID of the Trello card.
        
        Returns:
            dict: Card details including description.
        """
        url, params = self.build_url(f"cards/{card_id}")
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def extract_name_and_policy(self, card_name, card_description):
        """
        Extract person's name from description and policy number from card name.
        
        Args:
            card_name (str): The original card name (email subject).
            card_description (str): The card description (email body).
        
        Returns:
            tuple: (person_name, policy_number)
        """
        # Extract policy number (last 12 characters from card name)
        policy_number = card_name[-12:] if len(card_name) >= 12 else card_name
        
        # Extract person's name (first line of description)
        person_name = None
        should_process = False
        
        if card_description and card_description.strip():
            lines = card_description.split('\n')
            if lines:
                first_line = lines[0].strip()
                # Check if first line looks like a person's name
                # (has at least 2 words and doesn't look like email headers or generic text)
                if (first_line and 
                    len(first_line.split()) >= 2 and  # At least 2 words (first + last name)
                    not first_line.startswith(('Re:', 'Fwd:', 'Subject:', 'From:')) and  # Not email headers
                    not first_line.lower().startswith(('hola', 'buenos', 'buen', 'estimado'))):  # Not greetings
                    person_name = first_line
                    should_process = True
        
        return person_name, policy_number, should_process