"""crm_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# crm_project/urls.py

# crm_app/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import QuotationDataViewSet, QuotationTemplateViewSet,PermissionsViewSet, TextMessageViewSet,EmailAttachmentViewSet,EmailTemplateUpdateView,EmailTemplateViewSet, LeadViewSet,StatusChangeLogViewSet,LeadTimelineHistory,LeadTimelineupdated,LeadStatusViewSet,MeetingStatusChangeLogViewSet,BasicActivityInformationViewSet,leadtimeline,update_lead,PrintTimelineView, EmailSpecificFieldsViewSet, MeetingViewSet, LoginView

router = DefaultRouter()
router.register(r'leads', LeadViewSet)
router.register(r'lead-status', LeadStatusViewSet)
router.register(r'activities', BasicActivityInformationViewSet)
router.register(r'email-details', EmailSpecificFieldsViewSet)
router.register(r'meetings', MeetingViewSet)
router.register(r'status-change-logs', StatusChangeLogViewSet)
router.register(r'Meeting-Status-ChangeLog',MeetingStatusChangeLogViewSet)
router.register(r'email-template',EmailTemplateViewSet)
router.register(r'email-attachment', EmailAttachmentViewSet)
router.register(r'text-messages', TextMessageViewSet)
router.register(r'permissions', PermissionsViewSet)
router.register(r'quotation-data', QuotationDataViewSet, basename='quotation-data')
router.register(r'quotation-templates', QuotationTemplateViewSet, basename='quotation-template')



urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('leads/<int:pk>/', update_lead, name='update-lead'),
    path('email-templates/<int:pk>/', EmailTemplateUpdateView.as_view(), name='email-template-update'),
    path('timeline/', PrintTimelineView.as_view(), name='PrintTimelineView'),  
    path('timeline/<int:id>/', leadtimeline.as_view(), name='PrintTimelineView'),
    path('timelineu/<int:id>/',LeadTimelineupdated.as_view(), name="print"),
    path('timelineh',LeadTimelineHistory.as_view(), name="history")
]

#status = models.CharField(max_length=20, choices=[('Planned', 'Planned'), ('In Progress', 'In Progress'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], help_text="Status", default="Planned")
   