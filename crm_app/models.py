from django.db import models
from django.utils import timezone 
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import secrets
import string

class Lead(models.Model):
    COLOR_CHOICES = [
        ('#FF5733', 'Red'),
        ('#33FF6C', 'Green'),
        ('#337CFF', 'Blue'),
        ('#FF33EB', 'Pink'),
        ('#FFC233', 'Yellow'),
    ]
    organization = models.CharField(max_length=255, help_text="Organization name", null=True, blank=True, default=None)
    contact_name = models.CharField(max_length=255, help_text="Contact Name", null=True, blank=True, default=None)
    email = models.EmailField(help_text="Email address", blank=True, null=True, default=None)
    secondary_email = models.EmailField(help_text="Secondary email address", blank=True, null=True, default=None)
    phone = models.CharField(max_length=10, help_text="Phone number", blank=True, null=True, default=None)
    secondary_phone = models.CharField(max_length=10, help_text="Secondary Phone number", blank=True, null=True, default=None)
    requirement = models.TextField(help_text="Requirement details", null=True, blank=True, default=None)
    rating = models.IntegerField(help_text="Rating (e.g., 1, 2, 3, 4, 5)", default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    compliance = models.CharField(max_length=5, choices=[('No', 'No'), ('Yes', 'Yes')], help_text="Compliance status", null=True, blank=True, default=None)
    color_label = models.CharField(max_length=7, choices=COLOR_CHOICES, default='#FFFFFF', help_text="Color label for visualization", null=True, blank=True)
    source = models.CharField(max_length=100, choices=[('website', 'Website'), ('referral', 'Referral'), ('ads', 'Ads'), ('social', 'Social Media'), ('other', 'Other')], default='website', blank=True)
    lead_quality = models.CharField(max_length=50, choices=[('hot', 'Hot'), ('warm', 'Warm'), ('cold', 'Cold'), ('junk', 'Junk')], default='warm', blank=True)
    notes = models.TextField(blank=True, null=True, help_text="Additional notes or comments about this lead.", default=None)
    website = models.URLField(blank=True, null=True, help_text="The website URL of the lead.", default=None)
    street_address = models.CharField(max_length=255, help_text="Street Address (e.g., 123 Main St)", null=True, blank=True, default=None)
    suite_apartment_unit = models.CharField(max_length=255, help_text="Suite/Apartment/Unit Number", null=True, blank=True, default=None)
    city = models.CharField(max_length=100, help_text="City", null=True, blank=True, default=None)
    state = models.CharField(max_length=100, help_text="State/Province", null=True, blank=True, default=None)
    zip_postal_code = models.CharField(max_length=20, help_text="ZIP/Postal Code", null=True, blank=True, default=None)
    country = models.CharField(max_length=100, help_text="Country", default="India", blank=True)

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
    sender_name = models.CharField(max_length=255, help_text="Who sent the mail")
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
    name = models.FileField(upload_to='attachments', help_text="Attachments", null=True, blank=True)
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
    mail_sent = models.BooleanField(default=False)
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
    company_name = models.CharField(max_length=100, blank=True, null=True, help_text="Company name")
    position = models.CharField(max_length=100, blank=True, null=True, help_text="Job position")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    # Optional: Save the Profile model when the User is created (signals)
    def save(self, *args, **kwargs):
        if not self.pk:
            # Automatically create profile when user is created
            super(Profile, self).save(*args, **kwargs)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

class Permissions(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='permissions')  # Link to Profile
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

        
from django.db import models


class QuotationData(models.Model):
    organization = models.CharField(max_length=255)
    discription = models.TextField(null=True, blank=True)
    site_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    letter_head = models.ImageField(upload_to='letterheads/', null=True, blank=True)  # Image field for letterhead
    table_width = models.CharField(max_length=50, default='90%')  # For table width
    table_margin = models.CharField(max_length=50, default='200px auto')  # For table margin
    terms_and_conditions = models.TextField(null=True, blank=True)  # For terms and conditions

    # Salary fields
    basic_wages = models.CharField(max_length=60, blank=True, null=True)
    da = models.CharField(max_length=60, blank=True, null=True)
    hra = models.CharField(max_length=60, blank=True, null=True)
    special_allowance = models.CharField(max_length=60, blank=True, null=True)
    other_allowance = models.CharField(max_length=60, blank=True, null=True)
    extra_hours = models.CharField(max_length=60, blank=True, null=True)
    subtotal = models.CharField(max_length=60, blank=True, null=True)
    employee_pf = models.CharField(max_length=60, blank=True, null=True)
    employee_esic = models.CharField(max_length=60, blank=True, null=True)
    lwf1 = models.CharField(max_length=60, blank=True, null=True)
    professional_tax1 = models.CharField(max_length=60, blank=True, null=True)
    total_deduction = models.CharField(max_length=60, blank=True, null=True)
    in_hand_salary = models.CharField(max_length=60, blank=True, null=True)
    employer_pf = models.CharField(max_length=60, blank=True, null=True)
    employer_esic = models.CharField(max_length=60, blank=True, null=True)
    lwf2 = models.CharField(max_length=60, blank=True, null=True)
    professional_tax2 = models.CharField(max_length=60, blank=True, null=True)
    bonus = models.CharField(max_length=60, blank=True, null=True)
    gratuity = models.CharField(max_length=60, blank=True, null=True)
    national_leave = models.CharField(max_length=60, blank=True, null=True)
    paid_leave = models.CharField(max_length=60, blank=True, null=True)
    maintenance_cost = models.CharField(max_length=60, blank=True, null=True)
    total_i = models.CharField(max_length=60, blank=True, null=True)
    reliever_cost = models.CharField(max_length=60, blank=True, null=True)
    total_ii = models.CharField(max_length=60, blank=True, null=True)
    service_charge = models.CharField(max_length=60, blank=True, null=True)
    total_cost = models.CharField(max_length=60, blank=True, null=True)
    
    value_basic_wages = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    value_da = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    value_hra = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    value_special_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    value_other_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    value_extra_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    value_subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    Percentage_employee_pf = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    Percentage_employee_esic = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    value_lwf1 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    value_professional_tax1 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    value_total_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    value_in_hand_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    Percentage_employer_pf = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    Percentage_employer_esic = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    value_lwf2 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    value_professional_tax2 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    Percentage_bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    Percentage_gratuity = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    Percentage_national_leave = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    value_paid_leave = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    value_maintenance_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    value_total_i = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    Percentage_reliever_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    value_total_ii = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    Percentage_service_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    value_total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Salary details for {self.employee_id} in {self.organization}"


from django.db import models
from django.contrib.auth.models import User

class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="settings")
    theme_color = models.CharField(max_length=7,blank=True,null=True,help_text="The user's preferred theme color (e.g., #FFFFFF for white).")    
    language = models.CharField(max_length=50, default='en', help_text="The preferred language for the user.")
    meeting_notification = models.BooleanField(default=True,help_text="Whether the user wants to receive meeting notifications.")
    self_browser_notification = models.BooleanField(default=True, help_text="Whether the user wants to receive browser notifications.")
    self_sound_notification = models.BooleanField(default=True, help_text="Whether the user wants to receive sound notifications.")
    welcome_mail = models.BooleanField(default=False,help_text="Whether the user has received a welcome email." )
    MailSignature = models.ImageField(upload_to='MailSignature/', blank=True, null=True, help_text="Mail Footer")
    auto_refresh_duration = models.PositiveIntegerField( default=300, help_text="The duration (in seconds) for auto-refresh, default is 300 seconds (5 minutes).")

    def __str__(self):
        return f"Settings for {self.user.username}"

    def update_settings(self, **kwargs):
        """Convenience method to update settings."""
        for field, value in kwargs.items():
            if hasattr(self, field):
                setattr(self, field, value)
        self.save()

    class Meta:
        verbose_name = 'User Settings'
        verbose_name_plural = 'User Settings'



class ContactForm(models.Model):
    Name = models.CharField(max_length=40, blank=True, help_text="Data ID")
    url = models.CharField(max_length=8, unique=True, blank=True)
    
    Title = models.CharField(max_length=200, blank=True, help_text="Form title")
    enable_Title = models.BooleanField(default=True, help_text="Enable Title field")
    require_Title = models.BooleanField(default=False, help_text="Require Title field")
    
    Your_name = models.CharField(max_length=100, blank=True, help_text="Your name")
    enable_Your_name = models.BooleanField(default=True, help_text="Enable Your name field")
    require_Your_name = models.BooleanField(default=False, help_text="Require Your name field")
    
    Email = models.CharField(max_length=50, blank=True, help_text="Your email")
    enable_Email = models.BooleanField(default=True, help_text="Enable Email field")
    require_Email = models.BooleanField(default=False, help_text="Require Email field")
    
    Phone_number = models.CharField(max_length=50, blank=True, default='', help_text="Your phone number")
    enable_Phone_number = models.BooleanField(default=True, help_text="Enable Phone number field")
    require_Phone_number = models.BooleanField(default=False, help_text="Require Phone number field")

    Organization = models.CharField(max_length=50, blank=True, help_text="Your organization")
    enable_Organization = models.BooleanField(default=True, help_text="Enable Organization field")
    require_Organization = models.BooleanField(default=False, help_text="Require Organization field")
    
    location = models.CharField(max_length=50, blank=True, help_text="Subject")
    enable_location = models.BooleanField(default=True, help_text="Enable Subject field")
    require_location = models.BooleanField(default=False, help_text="Require Subject field")
    
    Message = models.CharField(max_length=50, blank=True, help_text="Message")
    enable_Message = models.BooleanField(default=True, help_text="Enable Message field")
    require_Message = models.BooleanField(default=False, help_text="Require Message field")

    inline_Label = models.BooleanField(default=False, help_text="Inline Label of Input Fields")

    style = models.TextField(blank=True, default='', help_text="CSS styling")
    Created_at = models.DateTimeField(auto_now_add=True, help_text="Creation timestamp")
    
    def save(self, *args, **kwargs):
        if not self.url:
            self.url = self.generate_random_url()
        super().save(*args, **kwargs)

    def generate_random_url(self):
        # Generate a random string with a combination of uppercase letters and digits
        characters = string.ascii_letters + string.digits
        random_url = ''.join(secrets.choice(characters) for _ in range(8))
        return random_url
    
    def __str__(self):
        return self.Subject
    class Meta:
        verbose_name_plural = "Contact Form"