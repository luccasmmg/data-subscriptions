import logging
import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

API_KEY = os.getenv("SENDGRID_API_KEY")
MAILER_FROM_EMAIL = os.getenv("MAILER_FROM_EMAIL")
MAILER_FROM_NAME = os.getenv("MAILER_FROM_NAME")
SENDGRID_TEMPLATE_ID = os.getenv("SENDGRID_TEMPLATE_ID")


class EmailDispatcher:
    def __init__(self, email):
        self.email = email
        self.client = SendGridAPIClient(API_KEY)
        self.message = Mail(
            from_email=(MAILER_FROM_EMAIL, MAILER_FROM_NAME),
            to_emails=self.email,
            subject="A dataset you have subscribed to has been updated",
        )

    def __call__(self, template_data):
        self.message.template_id = SENDGRID_TEMPLATE_ID
        self.message.dynamic_template_data = template_data
        try:
            self.response = self.client.send(self.message)
        except Exception as e:
            logging.error(e.body)
            raise e

        return self.response
