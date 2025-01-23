# Step 1: Install the required dependencies
# Ensure you have the following packages installed:
# pip install resend jinja2 loguru

from typing import List, Union
import resend
from jinja2 import Template
from loguru import logger
from pathlib import Path

# Step 2: Define the configuration settings for your email service
class Config:
    RESEND_API_KEY = "your-resend-api-key"  # Replace with your Resend API key
    SENDER_EMAIL = "your-sender-email@example.com"  # Replace with your sender's email
    SENDER_NAME = "Your Sender Name"  # Replace with your sender name
    TEMPLATE_BASE_PATH = Path("templates")  # Path to the folder containing email templates

# Step 3: Create a helper class to manage sending emails
class EmailService:
    def __init__(self, api_key: str, sender_email: str, sender_name: str):
        """
        Initialize the EmailService class.

        Args:
            api_key (str): The API key for the Resend service.
            sender_email (str): The sender's email address.
            sender_name (str): The name to be displayed as the sender.
        """
        resend.api_key = api_key
        self.sender_email = sender_email
        self.sender_name = sender_name
        self.template_base_path = Config.TEMPLATE_BASE_PATH

    def load_template(self, template_name: str) -> str:
        """
        Load an email template from a file.

        Args:
            template_name (str): Name of the template file (without extension).

        Returns:
            str: The content of the template file.

        Raises:
            FileNotFoundError: If the template file is not found.
        """
        template_path = self.template_base_path / f"{template_name}.html"
        try:
            with template_path.open("r", encoding="UTF-8") as file:
                return file.read()
        except FileNotFoundError:
            logger.error(f"Template not found: {template_path}")
            raise

    def render_template(self, template_name: str, data: dict) -> str:
        """
        Render an email template with the provided data.

        Args:
            template_name (str): Name of the template to render.
            data (dict): Dictionary of data to render into the template.

        Returns:
            str: Rendered HTML string.
        """
        html_template = self.load_template(template_name)
        jinja2_template = Template(html_template)
        return jinja2_template.render(**data)

    def send_email(self, recipients: Union[str, List[str]], subject: str, html_content: str):
        """
        Send an email using Resend.

        Args:
            recipients (Union[str, List[str]]): One or more recipient email addresses.
            subject (str): Subject of the email.
            html_content (str): HTML content of the email.
        """
        # Normalize recipients to always be a list
        recipients_list = recipients if isinstance(recipients, list) else [recipients]

        params = {
            "from": f"{self.sender_name} <{self.sender_email}>",
            "to": recipients_list,
            "subject": subject,
            "html": html_content
        }
        try:
            resend.Emails.send(params)
            logger.info(f"Email sent successfully to: {recipients_list}")
        except Exception as e:
            logger.error(f"Failed to send email to {recipients_list}: {str(e)}")

# Step 4: Demonstrate how to use the EmailService
if __name__ == "__main__":
    # Initialize the email service
    email_service = EmailService(
        api_key=Config.RESEND_API_KEY,
        sender_email=Config.SENDER_EMAIL,
        sender_name=Config.SENDER_NAME
    )

    # Prepare email data
    recipient = "recipient@example.com"  # Replace with the recipient's email
    subject = "Welcome to Our Service!"
    template_name = "welcome"  # Ensure there is a `welcome.html` template in the templates folder

    try:
        # Render the template with dynamic data
        template_data = {"username": "John Doe", "verification_link": "https://example.com/verify"}
        email_content = email_service.render_template(template_name, template_data)

        # Send the email
        email_service.send_email(recipients=recipient, subject=subject, html_content=email_content)
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
