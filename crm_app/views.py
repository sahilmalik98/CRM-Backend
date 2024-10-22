from rest_framework import viewsets
from django.http import HttpResponse
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import  QuotationData,QuotationTemplate,Permissions,TextMessage,EmailAttachment,Lead,MeetingStatusChangeLog,StatusChangeLog, BasicActivityInformation,EmailTemplate, EmailSpecificFields, Meeting,LeadStatus,SMS
from .serializers import QuotationDataSerializer,QuotationTemplateSerializer,PermissionsSerializer,TextMessageSerializer,EmailAttachmentSerializer,LeadStatusSerializer,MeetingStatusserializer,UserSerializer,StatusChangeLogSerializer, MyTokenObtainPairSerializer, LeadSerializer, BasicActivityInformationSerializer,EmailTemplateSerializer, EmailSpecificFieldsSerializer, MeetingSerializer
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from .serializers import MyTokenObtainPairSerializer
from datetime import datetime
import requests
from django.db.models import F, Value
from django.utils.timezone import make_aware, utc
import pandas as pd
import io
from .WelcomeMail import send_meeting_email, send_welcome_mail
import logging


logger = logging.getLogger(__name__)

class QuotationTemplateViewSet(viewsets.ModelViewSet):
    queryset = QuotationTemplate.objects.all()
    serializer_class = QuotationTemplateSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id', 'name']
    search_fields = ['name', 'description']
    ordering_fields = ['updated_at','created_at']

class QuotationDataViewSet(viewsets.ModelViewSet):
    queryset = QuotationData.objects.all()
    serializer_class = QuotationDataSerializer

class LeadStatusViewSet(viewsets.ModelViewSet):
    queryset = LeadStatus.objects.all()
    serializer_class = LeadStatusSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['lead',]

class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id', 'email']
    search_fields = ['organization', 'contact_name']
    ordering_fields = ['rating', 'win','created_at']

    def get_queryset(self):
        queryset = super().get_queryset()        
        # Custom filters from query parameters
        created_at = self.request.query_params.get('created_at', None)
        new_status = self.request.query_params.get('new_status', None)

        if created_at:
            queryset = queryset.filter(
                status_changes__changed_at__date=created_at
            ).distinct()

        if new_status:
            if new_status.startswith('!'):
                # Exclude leads with the specific new_status
                status_to_exclude = new_status[1:]  # Remove '!'
                queryset = queryset.exclude(
                    status_changes__new_status=status_to_exclude
                ).distinct()
            else:
                # Include leads with the specific new_status
                queryset = queryset.filter(
                    status_changes__new_status=new_status
                ).distinct()
        return queryset
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)  # Save the lead instance
        lead_instance = serializer.instance
        contact_name = serializer.validated_data.get('contact_name')
    
        # Prepare to send email in a try-except block, but do not halt creation on failure
        try:
            # Attempt to send the welcome email
            send_welcome_mail(contact_name, serializer.validated_data, lead_instance.id)
        except Exception as e:
            # Specific exception for template not found
            logger.error('Email template not found: %s', str(e))
            # Optionally, you could log a warning here but continue with the response
        except Exception as e:
            # Catch all other exceptions
            logger.error('Error sending email: %s', str(e))
            # Optionally log the error but do not return an error response here
    
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
def update_lead(request, pk):
    try:
        lead = Lead.objects.get(pk=pk)
    except Lead.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Update only provided fields
    serializer = LeadSerializer(lead, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BasicActivityInformationViewSet(viewsets.ModelViewSet):
    queryset = BasicActivityInformation.objects.all()
    serializer_class = BasicActivityInformationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['activity_type','lead', 'id']
    search_fields = ['activity_title', 'description']
    ordering_fields = ['priority', 'due_date']
    
class StatusChangeLogViewSet(viewsets.ModelViewSet):
    queryset = StatusChangeLog.objects.all()
    serializer_class = StatusChangeLogSerializer
    
class EmailAttachmentViewSet(viewsets.ModelViewSet):
    queryset = EmailAttachment.objects.all()
    serializer_class = EmailAttachmentSerializer

class EmailSpecificFieldsViewSet(viewsets.ModelViewSet):
    queryset = EmailSpecificFields.objects.all()
    serializer_class = EmailSpecificFieldsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id','mail_type','lead']
    search_fields = ['id', 'mail_type']
    ordering_fields = ['created_at']

class EmailTemplateViewSet(viewsets.ModelViewSet):
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name','id',]
    search_fields = ['name', 'body']
    ordering_fields = ['name',]
    
class EmailTemplateUpdateView(generics.UpdateAPIView):
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'id']
    search_fields = ['name', 'body']
    ordering_fields = ['template_type']
    

class MeetingStatusChangeLogViewSet(viewsets.ModelViewSet):
    queryset = MeetingStatusChangeLog.objects.all()
    serializer_class = MeetingStatusserializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        meeting_instance = serializer.validated_data.get('meeting')
        
        # Ensure you get the ID correctly
        if meeting_instance:
            idd = meeting_instance.id
        else:
            raise ValueError("Meeting instance not found")
        try:
            send_meeting_email(serializer.validated_data, idd)
   
        except Exception as e:
            print('Error sending email:', str(e))  # Log the specific error
            return Response({'error': 'Failed to send email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id','lead','meeting_date', 'meeting_type']
    search_fields = ['meeting_title', 'meeting_description']
    ordering_fields = ['meeting_date', 'start_time']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        created_at = self.request.query_params.get('created_at', None)
        new_status = self.request.query_params.get('new_status', None)

        if created_at and new_status:
            queryset = queryset.filter(
                status_changes__created_at__startswith=created_at,
                status_changes__new_status=new_status
            )

        return queryset
    
class TextMessageViewSet(viewsets.ModelViewSet):
    queryset = TextMessage.objects.all()
    serializer_class = TextMessageSerializer
    


class PermissionsViewSet(viewsets.ModelViewSet):
    queryset = Permissions.objects.all()
    serializer_class = PermissionsSerializer
    
class PrintTimelineView(APIView):
    def get(self, request, *args, **kwargs):
        activities = BasicActivityInformation.objects.all().values(
            type=Value('Activity'),
            status_changes_data=F('status_changes'),
            timestamp=F('created_at'),
            activity_titles=F('activity_title'),
            description_text=F('description'),
            activity_priority=F('priority')
        )
        
        status_changes = LeadStatus.objects.all().values(
            type=Value('Status Change'),
            timestamp=F('changed_at'),
            previous_status=F('old_status'),
            current_status=F('new_status'),
            status_feedback=F('feedback')
        )
        
        emails = EmailSpecificFields.objects.all().values(
            type=Value('Email'),
            email_sender=F('sender'),
            email_recipients=F('recipients'),
            email_subject=F('template__subject'),
            email_feedback=F('feedback')
        )
        
        meetings = Meeting.objects.all().values(
            type=Value('Meeting'),
            timestamp=F('created_at'),
            meeting_titles=F('meeting_title'),
            meeting_description_text=F('meeting_description'),
        
            meeting_attendees=F('attendees'),
            meeting_feedback=F('feedback')
        )
        
        sms = SMS.objects.all().values(
            type=Value('SMS'),
            sms_sender=F('sender'),
            sms_recipients=F('recipients'),
            sms_message=F('message'),
            sms_feedback=F('feedback')
        ) 
    
        all_data = list(activities) + list(status_changes) + list(emails) + list(meetings) + list(sms)
    
        # Provide a default datetime if 'timestamp' is None
        def safe_timestamp(item):
            timestamp = item['timestamp'] or datetime.min.replace(tzinfo=utc)
            if timestamp.tzinfo is None or timestamp.tzinfo.utcoffset(timestamp) is None:
                return make_aware(timestamp, timezone=utc)
            return timestamp
    
        sorted_data = sorted(all_data, key=safe_timestamp, reverse=True)
    
        # Optionally, format the data nicely using pandas
        df = pd.DataFrame(sorted_data)
        output = io.StringIO()
        df.to_string(output, index=False)
        
        response = output.getvalue()
        return Response(sorted_data, status=status.HTTP_200_OK)
    


class leadtimeline(APIView):
    def get(self, request, id, *args, **kwargs):
        # Fetch activities and their related status changes
        activities = BasicActivityInformation.objects.filter(lead=id).prefetch_related('status_changes')

        # Prepare list for final output
        activity_data = []

        # Process activities and their status changes
        for activity in activities:
            status_changes = activity.status_changes.all()

            # Create separate entries for each status change
            for change in status_changes:
                activity_entry = {
                    'type': 'Activity',
                    'activity_id': activity.id,
                    'timestamp': change.changed_at,
                    'activity_titles': activity.activity_title,
                    'description_text': activity.description,
                    'activity_priority': activity.priority,
                    'to': activity.assigned_to,
                    'activity_type' : activity.activity_type,
                    'status_changes_data': [
                        {
                            'old_status': change.old_status,
                            'new_status': change.new_status,
                            'changed_at': change.changed_at,
                            'changed_by': change.changed_by,
                            'feedback': change.feedback
                        }
                    ]
                }
                
                # Add the activity entry to the list
                activity_data.append(activity_entry)

   
        emails = EmailSpecificFields.objects.filter(lead=id)
        email_data = [
            {
                'type': 'Email',
                'timestamp': email.created_at,
                'email_sender': email.sender,
                'email_recipients': email.recipients,
                'email_subject': email.template.subject if email.template else None,
                'email_feedback': email.feedback
            }
            for email in emails
        ]

        meetings = Meeting.objects.filter(lead=id).prefetch_related('status_changes')
        # Prepare list for meeting data
        meeting_data = []
        
        # Process meetings and their status changes
        for meeting in meetings:
            status_changes = meeting.status_changes.all()
        
            # Create separate entries for each status change
            for change in status_changes:
                meeting_entry = {
                    'meeting_id': meeting.id,
                    'type': 'Meeting',
                    'timestamp': change.created_at,
                    'meeting_titles': meeting.meeting_title,
                    'meeting_description_text': meeting.meeting_description,
                    'meeting_attendees': meeting.attendees,
                    'meeting_feedback': meeting.feedback,
                    'status_changes_data': [
                        {
                            'old_status': change.old_status,
                            'new_status': change.new_status,
                            'changed_at': change.created_at,
                            'changed_by': change.changed_by,
                            'feedback': change.feedback
                        }
                    ]
                }
                
                # Add the meeting entry to the list
                meeting_data.append(meeting_entry)
        
        # Fetch other types of data
        status_changes = LeadStatus.objects.filter(lead=id)
        status_change_data = [
            {
                'type': 'Status Change',
                'timestamp': change.changed_at,
                'previous_status': change.old_status,
                'current_status': change.new_status,
                'status_feedback': change.feedback,
            }
            for change in status_changes
        ]

        
        # Combine all data
        all_data = activity_data + status_change_data + email_data + meeting_data
    
        # Provide a default datetime if 'timestamp' is None
        def safe_timestamp(item):
            timestamp = item['timestamp'] or datetime.min.replace(tzinfo=utc)
            if timestamp.tzinfo is None or timestamp.tzinfo.utcoffset(timestamp) is None:
                return make_aware(timestamp, timezone=utc)
            return timestamp
    
        sorted_data = sorted(all_data, key=safe_timestamp, reverse=True)
    
        # Optionally, format the data nicely using pandas
        df = pd.DataFrame(sorted_data)
        output = io.StringIO()
        df.to_string(output, index=False)
        
        response = output.getvalue()
        return Response(sorted_data, status=status.HTTP_200_OK)
    

class LeadTimelineupdated(APIView):
    def get(self, request, id, *args, **kwargs):
        try:
            # Fetch activities and their related status changes
            activities = BasicActivityInformation.objects.filter(lead=id).prefetch_related('status_changes')

            activity_data = []
            for activity in activities:
                status_changes = activity.status_changes.all()
                if status_changes:
                    most_recent_change = sorted(status_changes, key=lambda x: x.changed_at, reverse=True)[0]
                    timestamp = most_recent_change.changed_at
                else:
                    timestamp = activity.created_at
                activity_entry = {
                    'type': 'Activity',
                    'activity_id': activity.id,
                    'timestamp': timestamp, 
                    'activity_titles': activity.activity_title,
                    'description_text': activity.description,
                    'activity_priority': activity.priority,
                    'to': activity.assigned_to,
                    'activity_type': activity.activity_type,
                    'status_changes_data': sorted(
                        [
                            {
                                'old_status': change.old_status,
                                'new_status': change.new_status,
                                'changed_at': change.changed_at,
                                'changed_by': change.changed_by,
                                'feedback': change.feedback
                            }
                            for change in status_changes
                        ],
                        key=lambda x: x['changed_at'],
                        reverse=True
                    )
                }
                activity_data.append(activity_entry)

            # Fetch emails
            emails = EmailSpecificFields.objects.filter(lead=id)
            email_data = [
                {
                    'type': 'Email',
                    'timestamp': email.created_at,
                    'email_sender': email.sender,
                    'email_recipients': email.recipients,
                    'mail_type': email.mail_type,
                    #'email_subject': email.template.subject if email.template else None,
                    'email_feedback': email.feedback
                }
                for email in emails
            ]

            # Fetch meetings and their status changes
            meetings = Meeting.objects.filter(lead=id).prefetch_related('status_changes')
            meeting_data = []
            
            for meeting in meetings:
                status_changes = meeting.status_changes.all()
                if status_changes:
                    most_recent_change = sorted(status_changes, key=lambda x: x.created_at, reverse=True)[0]
                    timestamp = most_recent_change.created_at
                else:
                    timestamp = meeting.created_at 
                meeting_entry = {
                    'type': 'Meeting',
                    'meeting_id': meeting.id,
                    'timestamp': timestamp,
                    'meeting_titles': meeting.meeting_title,
                    'meeting_description_text': meeting.meeting_description,
                    'meeting_attendees': meeting.attendees,
                    'meeting_feedback': meeting.feedback,
                    'status_changes_data': sorted(
                        [
                            {
                                'old_status': change.old_status,
                                'new_status': change.new_status,
                                'created_at': change.created_at,
                                'changed_by': change.changed_by,
                                'feedback': change.feedback
                            }
                            for change in status_changes
                        ],
                        key=lambda x: x['created_at'],
                        reverse=True
                    )
                }
                meeting_data.append(meeting_entry)

            # Fetch status changes
            status_changes = LeadStatus.objects.filter(lead=id)
            status_change_data = sorted(
                [
                    {
                        'type': 'Status Change',
                        'timestamp': change.changed_at,
                        'previous_status': change.old_status,
                        'current_status': change.new_status,
                        'status_feedback': change.feedback
                    }
                    for change in status_changes
                ],
                key=lambda x: x['timestamp'],
                reverse=True
            )

            # Combine all data
            all_data = {
                'activities': activity_data,
                'status_changes': status_change_data,
                'emails': email_data,
                'meetings': meeting_data
            }

            # Flatten the data into a list
            flattened_data = []
            for key, items in all_data.items():
                for item in items:
                    item['category'] = key  # Add a category field for sorting
                    flattened_data.append(item)

            # Provide a default datetime if 'timestamp' is None
            def safe_timestamp(item):
                timestamp = item.get('timestamp')
                if not timestamp:
                    return datetime.min.replace(tzinfo=utc)
                if timestamp.tzinfo is None or timestamp.tzinfo.utcoffset(timestamp) is None:
                    return make_aware(timestamp, timezone=utc)
                return timestamp

            # Sort the data by timestamp in descending order
            sorted_data = sorted(flattened_data, key=safe_timestamp, reverse=True)

            return Response(sorted_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    
class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            user = User.objects.get(username=request.data['username'])
            refresh = RefreshToken.for_user(user)
            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        
        
        
        

class LeadTimelineHistory(APIView):
    def get(self, request, *args, **kwargs):
        try:
            
            # Fetch activities and their related status changes
            '''
            activities = BasicActivityInformation.objects.all().prefetch_related('status_changes')

            activity_data = []
            for activity in activities:
                status_changes = activity.status_changes.all()
                if status_changes:
                    most_recent_change = sorted(status_changes, key=lambda x: x.changed_at, reverse=True)[0]
                    timestamp = most_recent_change.changed_at
                else:
                    timestamp = activity.created_at
                activity_entry = {
                    'type': 'Activity',
                    'activity_id': activity.id,
                    'timestamp': timestamp, 
                    'activity_titles': activity.activity_title,
                    'description_text': activity.description,
                    'activity_priority': activity.priority,
                    'to': activity.assigned_to,
                    'activity_type': activity.activity_type,
                    'status_changes_data': sorted(
                        [
                            {
                                'old_status': change.old_status,
                                'new_status': change.new_status,
                                'changed_at': change.changed_at,
                                'changed_by': change.changed_by,
                                'feedback': change.feedback
                            }
                            for change in status_changes
                        ],
                        key=lambda x: x['changed_at'],
                        reverse=True
                    )
                }
                activity_data.append(activity_entry)
            '''

            # Fetch meetings and their status changes
            meetings = Meeting.objects.all().prefetch_related('status_changes')
            meeting_data = []
            
            for meeting in meetings:
                status_changes = meeting.status_changes.all()
                
                if status_changes:
                    # Sort the status changes in reverse order and get the first item
                    sorted_status_changes = sorted(status_changes, key=lambda x: x.created_at, reverse=True)
                    most_recent_change = sorted_status_changes[0]  # Get the first item in the reversed list
                    timestamp = most_recent_change.created_at
                    
                    meeting_entry = {
                        'type': 'Meeting',
                        'meeting_id': meeting.id,
                        'timestamp': timestamp,
                        'meeting_titles': meeting.meeting_title,
                        'meeting_description_text': meeting.meeting_description,
                        'meeting_attendees': meeting.attendees,
                        'meeting_feedback': meeting.feedback,
                        'status_changes_data': [
                            {
                                'id': most_recent_change.id,
                                'old_status': most_recent_change.old_status,
                                'new_status': most_recent_change.new_status,
                                'created_at': most_recent_change.created_at,
                                'changed_by': most_recent_change.changed_by,
                                'feedback': most_recent_change.feedback
                            }
                        ]
                    }
                    meeting_data.append(meeting_entry)
            
                        
                        # Fetch status changes
                      

            # Combine all data
            all_data = {
                #'activities': activity_data,
                'meetings': meeting_data
            }

            # Flatten the data into a list
            flattened_data = []
            for key, items in all_data.items():
                for item in items:
                    item['category'] = key  # Add a category field for sorting
                    flattened_data.append(item)

            # Provide a default datetime if 'timestamp' is None
            def safe_timestamp(item):
                timestamp = item.get('timestamp')
                if not timestamp:
                    return datetime.min.replace(tzinfo=utc)
                if timestamp.tzinfo is None or timestamp.tzinfo.utcoffset(timestamp) is None:
                    return make_aware(timestamp, timezone=utc)
                return timestamp

            # Sort the data by timestamp in descending order
            sorted_data = sorted(flattened_data, key=safe_timestamp, reverse=True)

            return Response(sorted_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
       
    
