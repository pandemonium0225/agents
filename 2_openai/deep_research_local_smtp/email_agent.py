from typing import Dict

import smtplib
from email.message import EmailMessage
from agents import Agent, function_tool


@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """Send an email with the given subject and HTML body"""
    msg = EmailMessage()
    msg["From"] = "test@local.dev"
    msg["To"] = "sean@local.dev"
    msg["Subject"] = subject
    msg.set_content("This is an HTML email. Please view in an HTML-capable client.")
    msg.add_alternative(html_body, subtype="html")

    with smtplib.SMTP("localhost", 1987) as smtp:
        smtp.send_message(msg)

    print("Email delivered to local SMTP (localhost:1987)")
    return "success"


INSTRUCTIONS = """You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report. You should use your tool to send one email, providing the 
report converted into clean, well presented HTML with an appropriate subject line."""

email_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model="gpt-4o-mini",
)
