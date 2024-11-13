
# crm_app/admin.py

from django.contrib import admin
from .models import UserSettings,Profile,Permissions, TextMessage,EmailAttachment,EmailTemplate,Lead, BasicActivityInformation, EmailSpecificFields, Meeting, StatusChangeLog, MeetingStatusChangeLog, LeadStatus


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'email', 'company_name', 'position', 'created_at', 'updated_at')
    search_fields = ('user__username', 'phone', 'email', 'company_name')
    list_filter = ('created_at', 'updated_at')
    #readonly_fields = ('user',)  # Make the user field read-only, since it's automatically set

admin.site.register(Profile, ProfileAdmin)

@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'theme_color', 'language', 
        'meeting_notification', 'self_browser_notification', 'self_sound_notification', 
        'welcome_mail', 'auto_refresh_duration'
    ]
    search_fields = ['user__username']

class activityStatusChangeLog(admin.StackedInline):
    model = StatusChangeLog
    extra = 0
    
class MeetingAdmininline(admin.StackedInline):
    model = MeetingStatusChangeLog
    extra = 0
    
class statuschangesinline(admin.StackedInline):
    model = LeadStatus
    extra = 0

class LeadAdmin(admin.ModelAdmin):
    inlines = [statuschangesinline]
    list_display = ('organization', 'contact_name', 'email', 'phone', 'rating', 'compliance')
    search_fields = ('organization', 'contact_name', 'email', 'phone')
    list_filter = ('rating', 'compliance')
admin.site.register(Lead, LeadAdmin)

class BasicActivityInformationAdmin(admin.ModelAdmin):
    inlines = [activityStatusChangeLog]
    list_display = ('activity_type','lead','assigned_to', 'activity_title', 'description', 'priority', 'due_date', 'start_time', 'end_time', 'duration')
    search_fields = ('activity_type', 'assigned_to', 'activity_title', 'description')
    list_filter = ('activity_type', 'priority')
admin.site.register(BasicActivityInformation, BasicActivityInformationAdmin)

@admin.register(Permissions)
class PermissionsAdmin(admin.ModelAdmin):
    list_display = ('user',)  # Customize as needed
    search_fields = ('user__username',)  # Assuming 'user' is a related field

@admin.register(TextMessage)
class TextMessageAdmin(admin.ModelAdmin):
    list_display = ('message_type', 'content', 'created_at', 'updated_at')  # Customize the fields displayed in the admin
    search_fields = ('message_type', 'content')  # Add search capability

class MeetingAdmin(admin.ModelAdmin):
    inlines = [MeetingAdmininline]
    list_display = ('meeting_title', 'meeting_description', 'meeting_date', 'start_time', 'end_time', 'duration', 'meeting_type', 'presenters')
    search_fields = ('meeting_title', 'meeting_description', 'attendees', 'presenters')
    list_filter = ('meeting_date', 'meeting_type')
admin.site.register(Meeting, MeetingAdmin)

class MeetingtemplateAdmin(admin.ModelAdmin):
    list_display = ('name','id')
admin.site.register(EmailTemplate, MeetingtemplateAdmin)

@admin.register(EmailSpecificFields)
class EmailSpecificFieldsAdmin(admin.ModelAdmin):
    # Optional: You can customize the admin interface for this model
    list_display = ('id','lead', 'sender', 'created_at')
    search_fields = ('sender', 'recipients', 'cc', 'bcc', 'body')
    list_filter = ('read_receipt', 'created_at')
    readonly_fields = ('created_at',)
    
@admin.register(EmailAttachment)
class EmailAttachmentadmin(admin.ModelAdmin):
    list_display = ('email','name')