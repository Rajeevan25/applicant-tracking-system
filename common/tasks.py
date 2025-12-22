from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


def send_email(subject: str, email: list[str], html_content: str, context: dict):
    # Logic to send a verification email to the user
    html_content = get_template(html_content).render(context) # Render the HTML content with context
    email_message = EmailMultiAlternatives(
        subject=subject, # Email subject
        body=html_content, # Email body content
        to=email,
        from_email="noreply@lkr.com"
    )
    email_message.send()