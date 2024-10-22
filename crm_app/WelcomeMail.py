# mail.py
import os
import smtplib
from django.utils import timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.image import MIMEImage
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
import mimetypes
from .models import Meeting, EmailTemplate, Lead, EmailSpecificFields
import logging

logger = logging.getLogger(__name__)

def send_welcome_mail(contact_name,form_data, leadid):
    smtp_server = 'mail.sahilmalik.tech'
    smtp_port    = 465
    smtp_user = 'sahil@sahilmalik.tech'
    smtp_password = 'Awer1234@#'
    from_email = 'sahil@sahilmalik.tech'

    try:
        mail_template = EmailTemplate.objects.get(template_type='welcome')
    except EmailTemplate.DoesNotExist:
        logger.error("Email template not found for template_type='welcome'")
        raise ValueError("Email template not found")

    logger.info(f"Person name: {contact_name}")
    logger.info(f"Email: {form_data['email']}")

    # Prepare the email notification
    notification_email = form_data['email']
    notification_body = mail_template.body.format(recipient_name=contact_name)
    sender_name = mail_template.name

    notification_msg = MIMEMultipart()
    notification_msg['From'] = f"{sender_name} <{from_email}>"
    notification_msg['To'] = notification_email
    notification_msg['Subject'] = mail_template.subject
    notification_msg.attach(MIMEText(notification_body, 'html'))

    lead_instance = Lead.objects.get(id=leadid)
    if mail_template.email_attachments.exists():
        for attachment in mail_template.email_attachments.all():
            try:
                file_path = attachment.file
                file_name = attachment.file.name
                content_type, _ = mimetypes.guess_type(file_name)
    
                if content_type is None:
                    content_type = 'application/octet-stream'
    
                print(f"Attaching file: {file_name}, Content Type: {content_type}")
    
                # Create a MIMEBase object
                mime_base = MIMEBase('application', content_type.split('/')[1])  # Use the correct subtype
                mime_base.set_payload(file_path.read())  # Set the payload to the file's content
                encoders.encode_base64(mime_base)  # Encode the payload
    
                # Add the header
                mime_base.add_header('Content-Disposition', f'attachment; filename="{file_name}"')
    
                # Attach the MIMEBase object to the message
                notification_msg.attach(mime_base)
            except Exception as e:
                logger.error(f"Error attaching file: {e}")
    
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_user, smtp_password)
            server.sendmail(from_email, notification_email, notification_msg.as_string())
            logger.info('Notification email sent successfully')

        # Save email log
        email_log = EmailSpecificFields(
            sender=from_email,
            recipients=notification_email,
            cc='',
            bcc='',
            body=notification_body,
            read_receipt=0,
            feedback='',
            lead=lead_instance,
            created_at=timezone.now(),
            mail_type='welcome'
        )
        email_log.save()
        logger.info('Email log saved successfully')

    except smtplib.SMTPException as smtp_error:
        logger.error(f"Failed to send notification email: {smtp_error}")
        raise  # Optionally raise the error to be handled higher up

    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        raise  # Optionally raise the error to be handled higher up


def send_meeting_email(form_data, idd):
    smtp_server = 'live.smtp.mailtrap.io'
    smtp_port = 587
    smtp_user = 'api'
    smtp_password = '84dde708439af8b37961bb85699435f1'
    from_email = 'smtp@mailtrap.io'

    try:
        MeetingDetails = Meeting.objects.get(id=idd)  # Use 'id' as keyword argument
        LeadDetails = Lead.objects.get(id= MeetingDetails.lead.id)
        MailTemplate = EmailTemplate.objects.get(template_type='meeting')
    except Meeting.DoesNotExist:
        raise ValueError("Meeting not found")
    except EmailTemplate.DoesNotExist:
        logger.error("Email template not found for template_type='meeting'")
        raise ValueError("Email template not found")
    
    # Prepare the email notification
    notification_email = 'mrsahilmalik98@gmail.com'
    notification_subject = 'New Form Submission Notification'
    namedetial = form_data['new_status']
    PersonName = LeadDetails.contact_name
    notification_body = MailTemplate.body.format(
        recipient_name = PersonName ,
        meeting_title = MeetingDetails.meeting_title,
        meeting_date = MeetingDetails.meeting_date,
        start_time = form_data['new_status'],
        meeting_type = form_data['new_status'],
        attendees = form_data['new_status'],
        new_status =  form_data['new_status'],
    )
    sender_name = MailTemplate.name
            
            
    notification_msg = MIMEMultipart()
    notification_msg['From'] = f"{sender_name} <{from_email}>"
    notification_msg['To'] = notification_email
    notification_msg['Subject'] = MailTemplate.subject
    notification_msg.attach(MIMEText(notification_body, 'html'))
    lead_instance = Lead.objects.get(id=MeetingDetails.lead.id)
    
    # Attach files from MailTemplate
    # Attach files from MailTemplate
    if MailTemplate.email_attachments.exists():
        for attachment in MailTemplate.email_attachments.all():
            try:
                file_path = attachment.file
                file_name = attachment.file.name
                content_type, _ = mimetypes.guess_type(file_name)
    
                if content_type is None:
                    content_type = 'application/octet-stream'
    
                print(f"Attaching file: {file_name}, Content Type: {content_type}")
    
                # Create a MIMEBase object
                mime_base = MIMEBase('application', content_type.split('/')[1])  # Use the correct subtype
                mime_base.set_payload(file_path.read())  # Set the payload to the file's content
                encoders.encode_base64(mime_base)  # Encode the payload
    
                # Add the header
                mime_base.add_header('Content-Disposition', f'attachment; filename="{file_name}"')
    
                # Attach the MIMEBase object to the message
                notification_msg.attach(mime_base)
            except Exception as e:
                logger.error(f"Error attaching file: {e}")
    
    
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_user, smtp_password)
            server.sendmail(from_email, notification_email, notification_msg.as_string())
            logger.info('Notification email sent successfully')
        try: 
            email_log = EmailSpecificFields(
                sender='sahil@sahilmalik.tech',
                recipients= LeadDetails.email,
                cc='',
                bcc='',
                body= notification_body,
                read_receipt= 0,
                feedback= '',
                lead= lead_instance,
                created_at=timezone.now(),
                mail_type= 'meeting'
            )
            email_log.save()
        except Exception as e:
            logger.error(f"Email Record not saved: {e}")
            
    except Exception as e:
        logger.error(f"Failed to send notification email: {e} " )

  
'''
const name = "John Doe"; // Your name variable
const dateTime = new Date(); // Replace this with your actual date variable

// Format the date as desired (e.g., "October 8, 2024")
const formattedDate = dateTime.toLocaleString('en-US', {
  year: 'numeric',
  month: 'long',
  day: 'numeric',
});

// Insert the name and date into the template
const emailBody = template.replace("{name}", name) 
+ `\n\nDate: ${formattedDate}`; 

console.log(emailBody);

'''