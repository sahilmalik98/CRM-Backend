import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Set up the server settings
smtp_server = "smtp.office365.com"
smtp_port = 465  # Port for SSL
email_address = "mrsahilmalik98@outlook.com"
email_password = "Ikmps@100%"  # Replace with your actual password

# Create the email
msg = MIMEMultipart()
msg['From'] = email_address
msg['To'] = "mrsahilmalik98@gmail.com"
msg['Subject'] = "Subject of the Email"

# Add the email body
body = "This is the body of the email."
msg.attach(MIMEText(body, 'plain'))

# Set up the SMTP SSL server connection
server = smtplib.SMTP_SSL(smtp_server, smtp_port)

# Log in to the email account
server.login(email_address, email_password)

# Send the email
server.sendmail(email_address, "mrsahilmalik98@gmail.com", msg.as_string())

# Disconnect from the server
server.quit()

print("Email sent successfully!")
