import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(subject, body, to_email, from_email, smtp_server, smtp_port, login, password):
    # Create the message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection

        # Login to the server
        server.login(login, password)

        # Send the email
        server.sendmail(from_email, to_email, msg.as_string())

        # Close the server connection
        server.quit()

        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Example usage
if __name__ == "__main__":
    subject = "Test Email"
    body = "This is a test email sent from Python."
    to_email = "mrsahilmalik98@gmail.com"
    from_email = "your_email@gmail.com"
    smtp_server = "smtp-mail.outlook.com"
    smtp_port = 587
    login = "connect@labeledwaterbottles.com"
    password = "Lwb@2024"

    send_email(subject, body, to_email, from_email, smtp_server, smtp_port, login, password)
    
    