import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# SMTP configuration
smtp_server = 'smtp-mail.outlook.com'
smtp_port = 465 #587  # Use 465 for SSL
username = 'mrsahilmalik98@outlook.com'  # Your email address
password = 'cynrnzsneqznbume'       # Your email password or App Password

# Create the email
msg = MIMEMultipart()
msg['From'] = username
msg['To'] = 'mrsahilmalik98@gmail.com'  # Recipient's email address
msg['Subject'] = 'Test Email from Python'

# Email body
body = 'Hello! This is a test email sent using Python!'
msg.attach(MIMEText(body, 'plain'))

# Send the email
try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS
    server.login(username, password)
    server.send_message(msg)
    print('Email sent successfully!')
except Exception as e:
    print(f'Error sending email: {e}')
finally:
    server.quit()
