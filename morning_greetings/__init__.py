"""
The `morning_greetings` module can be used to automate greeting a list of contacts. It will
generate a message for each user it is given, and send them a personalized greeting.
"""

__version__ = "1.0.0"
__author__ = "Giorgio Salvemini (s351995@oslomet.no)"


from .contact_manager import *
from .logger import *
from .message_generator import *
from .message_sender import *

# define dunder all to allow importing classes
__all__ = [
    "ContactsManager",
    "ImportMode",
    "generate_message",
    "send_message",
    "get_logger",
]
