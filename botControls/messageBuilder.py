import json
from typing import Any, Dict

class MESSAGE_CLASS:
    def __init__(self, tx_id: str, msg_name: str, rx_id: str, content: Dict[str, Any]):
        """
        Initializes the message builder with the necessary attributes.

        Args:
            tx_id (str): The tx_id of the sender.
            msg_name (str): The name of the message.
            rx_id (str): The desination of the message.
            content (Dict[str, Any]): The content of the message, as a dictionary.
        """
        self.tx_id = tx_id
        self.msg_name = msg_name
        self.rx_id = rx_id
        self.content = content  # content is expected to be a dictionary or any JSON-serializable object
    
    def buildMessage(self) -> str:
        """
        Builds the message as a JSON string.

        Returns:
            str: The JSON-encoded message.
        """
        message = {
            'tx_id': self.tx_id,
            'rx_id': self.rx_id,
            'msg_name': self.msg_name,
            'content': self.content  # content is already a JSON-serializable object
        }
        return json.dumps(message)


