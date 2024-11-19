from rest_framework import serializers
from .models import ContactForm,UserSettings,Profile,QuotationData,Permissions,TextMessage,EmailAttachment,EmailTemplate,Lead, BasicActivityInformation, EmailSpecificFields, Meeting, User, StatusChangeLog, LeadStatus, MeetingStatusChangeLog
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['bio', 'phone', 'address', 'profile_picture']  # Add other fields as needed

class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = [
            'theme_color', 'language', 'meeting_notification', 
            'self_browser_notification', 'self_sound_notification', 
            'welcome_mail', 'auto_refresh_duration'
        ]

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)  # Nested ProfileSerializer
    settings = UserSettingsSerializer(read_only=True)  # Nested UserSettingsSerializer

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'profile', 'settings'  # Include profile and settings in the response
        ]

class ContactFormserializers(serializers.ModelSerializer):
    class Meta:
        model = ContactForm
        fields = '__all__'

class QuotationDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationData
        fields = '__all__'  # Include all fields

class LeadStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadStatus
        fields = '__all__'

class LeadSerializer(serializers.ModelSerializer):
    status_changes =LeadStatusSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Lead
        fields = '__all__'
    
        
class StatusChangeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusChangeLog
        fields = '__all__'

class BasicActivityInformationSerializer(serializers.ModelSerializer):
    status_changes = StatusChangeLogSerializer(many=True, read_only=True, required=False)
    class Meta:
        model = BasicActivityInformation
        fields = '__all__'

class EmailSpecificFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailSpecificFields
        fields = '__all__'

class EmailAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailAttachment
        fields = '__all__'

class EmailTemplateSerializer(serializers.ModelSerializer):
    email_attachments = EmailAttachmentSerializer(many=True, read_only=True, required=False)
    class Meta:
        model = EmailTemplate
        fields = '__all__'

class MeetingStatusserializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingStatusChangeLog
        fields = '__all__'
        
class MeetingSerializer(serializers.ModelSerializer):
    status_changes = MeetingStatusserializer(many=True, read_only=True, required=False)
    class Meta:
        model = Meeting
        fields = '__all__'

class TextMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextMessage
        fields = '__all__'  # Include all fields or specify the ones you want
    

class PermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permissions
        fields = '__all__'  # Include all fields or specify the ones you want

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        # Add any other custom fields here

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # You can add more data to the response here if needed
        data.update({'user': {
            'username': self.user.username,
            'email': self.user.email,
            # Add any other custom fields here
        }})

        return data