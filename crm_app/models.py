from django.db import models
from django.utils import timezone 
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class Lead(models.Model):
    COLOR_CHOICES = [
        ('#FF5733', 'Red'),
        ('#33FF6C', 'Green'),
        ('#337CFF', 'Blue'),
        ('#FF33EB', 'Pink'),
        ('#FFC233', 'Yellow'),
    ]
    organization = models.CharField(max_length=255, help_text="Organization name", null=True, blank=True)
    contact_name = models.CharField(max_length=255, help_text="Contact Name", null=True, blank=True)
    email = models.EmailField(help_text="Email address")
    phone = models.CharField(max_length=10, help_text="Phone number",)
    requirement = models.TextField(help_text="Requirement details", null=True, blank=True)
    rating = models.IntegerField(help_text="Rating (e.g., 1, 2, 3, 4, 5)", default=1, validators=[MinValueValidator(1),MaxValueValidator(5)])
    compliance = models.CharField(max_length=5, choices=[('No', 'No'), ('Yes', 'Yes')], help_text="Compliance status", null=True, blank=True)
    color_label = models.CharField(max_length=7, choices=COLOR_CHOICES, default='#FFFFFF', help_text="Color label for visualization", null=True, blank=True)
    
    street_address = models.CharField(max_length=255, help_text="Street Address (e.g., 123 Main St)", null=True, blank=True)
    suite_apartment_unit = models.CharField(max_length=255, help_text="Suite/Apartment/Unit Number", null=True, blank=True)
    city = models.CharField(max_length=100, help_text="City", null=True, blank=True)
    state_province = models.CharField(max_length=100, help_text="State/Province", null=True, blank=True)
    zip_postal_code = models.CharField(max_length=20, help_text="ZIP/Postal Code", null=True, blank=True)
    country = models.CharField(max_length=100, help_text="Country", default="India")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, help_text="Latitude", null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, help_text="Longitude", null=True, blank=True)
    
    created_at = models.DateTimeField(default=timezone.now, editable=False, help_text="Date and time when the profile was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date and time when the profile was last updated")
    def __str__(self):
        return f"{self.organization} - {self.contact_name}"
        # Optionally, you can override update() if you need custom behavior
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
class LeadStatus(models.Model):
    LEAD_STATUS_CHOICES = [
        ('New', 'New'),
        ('Qualified/Meeting', 'Qualified/Meeting'),
        ('Process', 'In Process'),
        ('Win', 'Win'), 
        ('Lost', 'Lost')
    ]
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='status_changes')
    old_status = models.CharField(max_length=20,choices=LEAD_STATUS_CHOICES,help_text="Previous lead status",null=True,blank=True)
    new_status = models.CharField(max_length=20,choices=LEAD_STATUS_CHOICES,default='New',help_text="Current lead status")
    changed_at = models.DateTimeField(auto_now=True, help_text="Date and time when the Status was last updated")
    changed_by = models.CharField(max_length=255, help_text="User who changed the status", null=True, blank=True)  # Optional field for tracking who made the change
    feedback = models.TextField(null=True, blank=True, help_text="Feedback regarding the lead status change")
    def __str__(self):
        return f"{self.new_status}"

class BasicActivityInformation(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='activities', null=True, blank=True)
    activity_type = models.CharField(max_length=50, choices=[('Email', 'Email'), ('Call', 'Call'), ('Meeting', 'Meeting'), ('To-Do', 'To-Do')], help_text="Activity Type", null=True, blank=True)
    assigned_to = models.CharField(max_length=255, help_text="Assigned To", null=True, blank=True)
    activity_title = models.CharField(max_length=255, help_text="Activity Title", null=True, blank=True)
    description = models.TextField(help_text="Description", null=True, blank=True)
    priority = models.CharField(max_length=10, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], help_text="Priority", null=True, blank=True)
    due_date = models.DateField(help_text="Due Date", null=True, blank=True)
    start_time = models.TimeField(help_text="Start Time", null=True, blank=True)
    end_time = models.TimeField(help_text="End Time", null=True, blank=True)
    duration = models.DurationField(help_text="Duration", null=True, blank=True)
    feedback = models.TextField(null=True, blank=True, help_text="Feedback regarding the lead status change")
    created_at = models.DateTimeField(default=timezone.now, editable=False, help_text="Date and time when the profile was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date and time when the profile was last updated")

class StatusChangeLog(models.Model):
    activity = models.ForeignKey(BasicActivityInformation, on_delete=models.CASCADE, related_name='status_changes')
    old_status = models.CharField(max_length=20, blank=True, null=True)
    new_status = models.CharField(max_length=20, blank=True, null=True)
    changed_at = models.DateTimeField(default=timezone.now, help_text="Date and time when the status change occurred")
    changed_by = models.CharField(max_length=255, help_text="User who changed the status", null=True, blank=True)  # Optional field for tracking who made the change
    feedback = models.TextField(null=True, blank=True, help_text="Feedback regarding the lead status change")
    def __str__(self):
        return f"Status changed from {self.old_status} to {self.new_status} on {self.changed_at}"

class EmailTemplate(models.Model):
    TEMPLATE_TYPES = [
        ('welcome', 'Welcome Email'),
        ('meeting', 'Meeting Email'),
        ('notification', 'Notification Email'),
        ('reminder', 'Reminder Email'),
        ('template', 'Template'),
    ]
    name = models.CharField(max_length=255, help_text="Template Name")
    subject = models.CharField(max_length=255, help_text="Email Subject")
    body = models.TextField(help_text="Email Body")
    template_type = models.CharField(max_length=50, choices=TEMPLATE_TYPES, default='template', help_text="Type of Email Template")
    created_at = models.DateTimeField(default=timezone.now, editable=False, help_text="Date and time when the template was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date and time when the template was last updated")
    def __str__(self):
        return self.name

class EmailSpecificFields(models.Model):
    MAIL_TYPES = [
        ('welcome', 'Welcome Email'),
        ('meeting', 'Meeting Email'),
        ('notification', 'Notification Email'),
        ('reminder', 'Reminder Email'),
        ('template', 'Template'),
    ]
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='email_details', null=True, blank=True)
    sender = models.EmailField(help_text="Sender", null=True, blank=True)
    recipients = models.TextField(help_text="Recipients", null=True, blank=True)
    cc = models.TextField(help_text="CC", null=True, blank=True)
    bcc = models.TextField(help_text="BCC", null=True, blank=True)
    body = models.TextField(help_text="Body", null=True, blank=True)
    mail_type = models.CharField(max_length=50, choices=MAIL_TYPES, default='template', help_text="Type of Email Template")
    read_receipt = models.BooleanField(help_text="Read Receipt", default=False, null=True, blank=True)
    feedback = models.TextField(null=True, blank=True, help_text="Feedback regarding the lead status change")
    created_at = models.DateTimeField(default=timezone.now, editable=False, help_text="Date and time when the profile was created")
    def __str__(self):
        return f"Email from {self.sender} to {self.recipients}"

class EmailAttachment(models.Model):
    email = models.ForeignKey(EmailTemplate, on_delete=models.CASCADE, related_name='email_attachments')
    file = models.FileField(upload_to='attachments', help_text="Attachments", null=True, blank=True)
    def __str__(self):
        return f"Attachment for email {self.email.subject if self.email else 'None'}"

class Meeting(models.Model):
    MEETING_STATUS_CHOICES = [
        ('Requested', 'Requested'),
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('Postponed', 'Postponed'),
    ]
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='meeting_details', null=True, blank=True)
    template = models.ForeignKey(EmailTemplate, on_delete=models.SET_NULL, null=True, blank=True, related_name='meetingemails', help_text="Email Template")
    read_receipt = models.BooleanField(help_text="Read Receipt if mail was sent", default=False, null=True, blank=True)
    meeting_title = models.CharField(max_length=255, help_text="Meeting Title", null=True, blank=True)
    meeting_description = models.TextField(help_text="Meeting Description", null=True, blank=True)
    meeting_date = models.DateField(help_text="Meeting Date", null=True, blank=True)
    start_time = models.TimeField(help_text="Start Time", null=True, blank=True)
    end_time = models.TimeField(help_text="End Time", null=True, blank=True)
    duration = models.DurationField(help_text="Duration", null=True, blank=True)
    meeting_type = models.CharField(max_length=20, choices=[('conference-call', 'conference call'), ('in-person', 'in person'), ('virtual', 'virtual')], help_text="Meeting Type", null=True, blank=True)
    attendees = models.TextField(help_text="Attendees", null=True, blank=True)
    presenters = models.TextField(help_text="Presenter(s)", null=True, blank=True)
    feedback = models.TextField(null=True, blank=True, help_text="Feedback regarding the lead status change")
    created_at = models.DateTimeField(default=timezone.now, editable=False, help_text="Date and time when the profile was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date and time when the profile was last updated")

class MeetingStatusChangeLog(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='status_changes')
    old_status = models.CharField(max_length=20, help_text="Previous meeting status", null=True,blank=True)
    new_status  = models.CharField( max_length=20, default='Scheduled', help_text="Current meeting status")
    feedback = models.TextField( null=True, blank=True, help_text="Feedback regarding the meeting status change")
    changed_by = models.CharField(max_length=255, help_text="User who changed the status", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the record was created")
    def __str__(self):
        return f"Meeting {self.meeting.id} changed status from {self.old_status} to {self.new_status} on {self.created_at}"

class SMS(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='sms_details', null=True, blank=True)
    sender = models.CharField(max_length=100, help_text="Sender's phone number", null=True, blank=True)
    recipients = models.TextField(help_text="Recipient's phone numbers (comma-separated)", null=True, blank=True)
    message = models.TextField(help_text="SMS message content", null=True, blank=True)
    feedback = models.TextField(null=True, blank=True, help_text="Feedback regarding the lead status change")
    created_at = models.DateTimeField(default=timezone.now, editable=False, help_text="Date and time when the profile was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date and time when the profile was last updated")
    def __str__(self):
        return f"SMS from {self.sender} sent at {self.sent_date_time}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True, help_text="Short bio")
    birth_date = models.DateField(blank=True, null=True, help_text="Date of birth")
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, help_text="Profile picture")
    phone = models.CharField(max_length=15, blank=True, null=True, help_text="Phone number")
    email = models.EmailField(blank=True, null=True, help_text="Email address")
    address = models.TextField(blank=True, null=True, help_text="Address details")
    created_at = models.DateTimeField(default=timezone.now, editable=False, help_text="Date and time when the profile was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date and time when the profile was last updated")


    def __str__(self):
        return f"Profile of {self.user.username}"

class Permissions(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='permissions')  # Link to Profile
    can_view_leads = models.BooleanField(default=False)
    can_add_leads = models.BooleanField(default=False)
    can_edit_leads = models.BooleanField(default=False)
    can_delete_leads = models.BooleanField(default=False)
    can_view_lead_status = models.BooleanField(default=False)
    can_edit_lead_status = models.BooleanField(default=False)
    can_view_timeline = models.BooleanField(default=False)
    can_create_meeting = models.BooleanField(default=False)
    can_edit_meeting = models.BooleanField(default=False)
    can_view_calendar = models.BooleanField(default=False)
    can_edit_calendar = models.BooleanField(default=False)
    can_send_sms = models.BooleanField(default=False)
    can_view_sms = models.BooleanField(default=False)
    can_view_email = models.BooleanField(default=False)
    can_edit_email = models.BooleanField(default=False)
    
    # New permissions
    can_view_meeting = models.BooleanField(default=False)
    can_view_quotation = models.BooleanField(default=False)
    can_send_mail = models.BooleanField(default=False)
    can_view_mail = models.BooleanField(default=False)
    can_analytics = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.user.username}'s Permissions"
    
class TextMessage(models.Model):
    INPUT_SUGGESTION = 'input_suggestion'
    ERROR_MESSAGE = 'error_message'
    
    # Define the choices for message types
    MESSAGE_TYPE_CHOICES = [
        (INPUT_SUGGESTION, 'Input Suggestion'),
        (ERROR_MESSAGE, 'Error Message'),
        # Add other message types as needed
    ]
    message_type = models.CharField(max_length=50, choices=MESSAGE_TYPE_CHOICES, default=INPUT_SUGGESTION)  # Optional: set a default value  # e.g., 'input_suggestion', 'error_message'
    content = models.TextField()  # The actual message content
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.message_type}: {self.content[:20]}..."  # Display a snippet of the message content

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True, help_text="Short bio")
    birth_date = models.DateField(blank=True, null=True, help_text="Date of birth")
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, help_text="Profile picture")
    phone = models.CharField(max_length=15, blank=True, null=True, help_text="Phone number")
    email = models.EmailField(blank=True, null=True, help_text="Email address")
    address = models.TextField(blank=True, null=True, help_text="Address details")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # Make sure to inherit from this in your UserProfile
        
        
from django.db import models

class QuotationTemplate(models.Model):
    name = models.CharField(max_length=255)  # Name of the quotation template
    description = models.TextField(blank=True, null=True)  # Description of the template
    letterhead_image = models.ImageField(upload_to='letterheads/', blank=True, null=True)  # Letterhead image
    margin_top = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)  # Margin for the template
    margin_left = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)
    organization = models.CharField(max_length=255)  # Organization name
    template_type = models.CharField(max_length=50)  # Type of the template (e.g., PDF, Word)
    created_at = models.DateTimeField(auto_now_add=True)  # Creation timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Update timestamp

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Quotation Template'
        verbose_name_plural = 'Quotation Templates'


class QuotationData(models.Model):
    particular_id = models.CharField(max_length=255)
    particular = models.CharField(max_length=255)  # Particular field
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount field
    percentage = models.DecimalField(max_digits=5, decimal_places=2)  # Percentage field
    enable = models.BooleanField(default=True)  # Enable field
    formula = models.TextField(blank=True, null=True)  # Formula field
    quotation_template = models.ForeignKey(QuotationTemplate, related_name='quotation_data_entries', on_delete=models.CASCADE)  # Mapping to QuotationTemplate

    def __str__(self):
        return f"{self.particular} - {self.amount}"

    class Meta:
        verbose_name = 'Quotation Data'
        verbose_name_plural = 'Quotation Data'
