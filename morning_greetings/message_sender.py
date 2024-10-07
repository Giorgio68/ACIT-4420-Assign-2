"""
This module simulates sending messages to a given email address, by printing the message to
console
"""

from .logger import get_logger


def send_message(email: str, message: str) -> None:
    """
    "Sends" the message to the provided email address

    :param email: The email address of the recipient
    :param message: The body of the email
    """

    if not email:
        raise ValueError("No email address was provided")

    if not isinstance(email, str):
        raise ValueError("`email` has an invalid data")

    if not message:
        raise ValueError("No message body was provided")

    if not isinstance(message, str):
        raise ValueError("`message` has an invalid data")

    # Simulate sending a message (replace this with actual email sending logic if needed)
    print(f"Sending message to {email}: {message}")
    get_logger().info("Sent email to %s with body %s", email, message)
