# Resend Email Service

A Python project that demonstrates how to send emails using the [Resend](https://resend.com/) API with templated HTML content. This project uses Jinja2 for rendering templates and Loguru for logging.

## Features

- **Email Sending**: Send emails using the Resend API.
- **Template Rendering**: Use Jinja2 to create dynamic, data-driven email templates.
- **Logging**: Monitor email sending with Loguru logging.

## Prerequisites

1. Python 3.7+
2. A Resend API key ([Sign up for Resend](https://resend.com/)).

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/GiapKun/send-mail-with-resend.git
   cd <send-mail-with-resend>
   ```

2. Install the required dependencies:

   ```bash
   pip install resend jinja2 loguru
   ```

3. Set up your email templates:

   - Create a `templates` folder in the project directory.
   - Add your email templates (e.g., `welcome.html`) to this folder.

4. Configure your API key and sender information:
   - Replace placeholders in the `Config` class with your values:
     ```python
     RESEND_API_KEY = "your-resend-api-key"  # Replace with your Resend API key
     SENDER_EMAIL = "your-sender-email@example.com"  # Replace with your sender's email
     SENDER_NAME = "Your Sender Name"  # Replace with your sender name
     ```

## Usage

### 1. Initialize the EmailService

```python
email_service = EmailService(
    api_key=Config.RESEND_API_KEY,
    sender_email=Config.SENDER_EMAIL,
    sender_name=Config.SENDER_NAME
)
```

### 2. Prepare Email Data

- Create a recipient email:
  ```python
  recipient = "recipient@example.com"
  ```
- Set the email subject:
  ```python
  subject = "Welcome to Our Service!"
  ```
- Specify the email template (e.g., `welcome.html`) and provide dynamic data:
  ```python
  template_name = "welcome"
  template_data = {"username": "John Doe", "verification_link": "https://example.com/verify"}
  ```

### 3. Render the Email Template

```python
email_content = email_service.render_template(template_name, template_data)
```

### 4. Send the Email

```python
email_service.send_email(recipients=recipient, subject=subject, html_content=email_content)
```

### Full Example

```python
if __name__ == "__main__":
    email_service = EmailService(
        api_key=Config.RESEND_API_KEY,
        sender_email=Config.SENDER_EMAIL,
        sender_name=Config.SENDER_NAME
    )

    recipient = "recipient@example.com"
    subject = "Welcome to Our Service!"
    template_name = "welcome"

    try:
        template_data = {"username": "John Doe", "verification_link": "https://example.com/verify"}
        email_content = email_service.render_template(template_name, template_data)
        email_service.send_email(recipients=recipient, subject=subject, html_content=email_content)
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
```

## Email Template Example

Save the following HTML template as `welcome.html` in the `templates` folder:

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Welcome</title>
  </head>
  <body>
    <h1>Welcome, {{ username }}!</h1>
    <p>
      Thank you for joining our service. Please verify your email address by
      clicking the link below:
    </p>
    <a href="{{ verification_link }}">Verify Email</a>
  </body>
</html>
```

## Logging

This project uses Loguru for logging. Log entries are displayed in the console, including errors and successful email sends.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

## Acknowledgments

- [Resend](https://resend.com/)
- [Jinja2](https://palletsprojects.com/p/jinja/)
- [Loguru](https://loguru.readthedocs.io/)
