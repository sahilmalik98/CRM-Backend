# Generated by Django 4.2.6 on 2024-06-05 11:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crm_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailspecificfields',
            name='activity',
        ),
        migrations.RemoveField(
            model_name='meeting',
            name='activity',
        ),
        migrations.AddField(
            model_name='basicactivityinformation',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, help_text='Date and time when the profile was created'),
        ),
        migrations.AddField(
            model_name='basicactivityinformation',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='Date and time when the profile was last updated'),
        ),
        migrations.AddField(
            model_name='emailspecificfields',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, help_text='Date and time when the profile was created'),
        ),
        migrations.AddField(
            model_name='emailspecificfields',
            name='lead',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='email_details', to='crm_app.lead'),
        ),
        migrations.AddField(
            model_name='emailspecificfields',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='Date and time when the profile was last updated'),
        ),
        migrations.AddField(
            model_name='lead',
            name='color_label',
            field=models.CharField(blank=True, choices=[('#FF5733', 'Red'), ('#33FF6C', 'Green'), ('#337CFF', 'Blue'), ('#FF33EB', 'Pink'), ('#FFC233', 'Yellow')], default='#FFFFFF', help_text='Color label for visualization', max_length=7, null=True),
        ),
        migrations.AddField(
            model_name='lead',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, help_text='Date and time when the profile was created'),
        ),
        migrations.AddField(
            model_name='lead',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='Date and time when the profile was last updated'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, help_text='Date and time when the profile was created'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='lead',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='meeting_details', to='crm_app.lead'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='Date and time when the profile was last updated'),
        ),
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(blank=True, help_text='City', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='country',
            field=models.CharField(default='India', help_text='Country', max_length=100),
        ),
        migrations.AlterField(
            model_name='address',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, help_text='Latitude', max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='lead',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='crm_app.lead'),
        ),
        migrations.AlterField(
            model_name='address',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, help_text='Longitude', max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='state_province',
            field=models.CharField(blank=True, help_text='State/Province', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='street_address',
            field=models.CharField(blank=True, help_text='Street Address (e.g., 123 Main St)', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='suite_apartment_unit',
            field=models.CharField(blank=True, help_text='Suite/Apartment/Unit Number', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='zip_postal_code',
            field=models.CharField(blank=True, help_text='ZIP/Postal Code', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='basicactivityinformation',
            name='activity_title',
            field=models.CharField(blank=True, help_text='Activity Title', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='basicactivityinformation',
            name='activity_type',
            field=models.CharField(blank=True, choices=[('Email', 'Email'), ('Call', 'Call'), ('Meeting', 'Meeting'), ('To-Do', 'To-Do')], help_text='Activity Type', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='basicactivityinformation',
            name='assigned_to',
            field=models.CharField(blank=True, help_text='Assigned To', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='basicactivityinformation',
            name='description',
            field=models.TextField(blank=True, help_text='Description', null=True),
        ),
        migrations.AlterField(
            model_name='basicactivityinformation',
            name='due_date',
            field=models.DateField(blank=True, help_text='Due Date', null=True),
        ),
        migrations.AlterField(
            model_name='basicactivityinformation',
            name='duration',
            field=models.DurationField(blank=True, help_text='Duration', null=True),
        ),
        migrations.AlterField(
            model_name='basicactivityinformation',
            name='end_time',
            field=models.TimeField(blank=True, help_text='End Time', null=True),
        ),
        migrations.AlterField(
            model_name='basicactivityinformation',
            name='lead',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='crm_app.lead'),
        ),
        migrations.AlterField(
            model_name='basicactivityinformation',
            name='priority',
            field=models.CharField(blank=True, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], help_text='Priority', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='basicactivityinformation',
            name='start_time',
            field=models.TimeField(blank=True, help_text='Start Time', null=True),
        ),
        migrations.AlterField(
            model_name='basicactivityinformation',
            name='status',
            field=models.CharField(choices=[('Planned', 'Planned'), ('In Progress', 'In Progress'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Planned', help_text='Status', max_length=20),
        ),
        migrations.AlterField(
            model_name='emailspecificfields',
            name='attachments',
            field=models.FileField(blank=True, help_text='Attachments', null=True, upload_to='attachments/'),
        ),
        migrations.AlterField(
            model_name='emailspecificfields',
            name='bcc',
            field=models.TextField(blank=True, help_text='BCC', null=True),
        ),
        migrations.AlterField(
            model_name='emailspecificfields',
            name='body',
            field=models.TextField(blank=True, help_text='Body', null=True),
        ),
        migrations.AlterField(
            model_name='emailspecificfields',
            name='cc',
            field=models.TextField(blank=True, help_text='CC', null=True),
        ),
        migrations.AlterField(
            model_name='emailspecificfields',
            name='read_receipt',
            field=models.BooleanField(blank=True, default=False, help_text='Read Receipt', null=True),
        ),
        migrations.AlterField(
            model_name='emailspecificfields',
            name='recipients',
            field=models.TextField(blank=True, help_text='Recipients', null=True),
        ),
        migrations.AlterField(
            model_name='emailspecificfields',
            name='sender',
            field=models.EmailField(blank=True, help_text='Sender', max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='emailspecificfields',
            name='sent_date_time',
            field=models.DateTimeField(blank=True, help_text='Sent Date and Time', null=True),
        ),
        migrations.AlterField(
            model_name='emailspecificfields',
            name='subject',
            field=models.CharField(blank=True, help_text='Subject', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='lead',
            name='compliance',
            field=models.CharField(blank=True, choices=[('No', 'No'), ('Yes', 'Yes')], help_text='Compliance status', max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='lead',
            name='contact_name',
            field=models.CharField(blank=True, help_text='Contact Name', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='lead',
            name='email',
            field=models.EmailField(help_text='Email address', max_length=254),
        ),
        migrations.AlterField(
            model_name='lead',
            name='organization',
            field=models.CharField(blank=True, help_text='Organization name', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='lead',
            name='phone',
            field=models.CharField(help_text='Phone number', max_length=10),
        ),
        migrations.AlterField(
            model_name='lead',
            name='rating',
            field=models.IntegerField(blank=True, help_text='Rating (e.g., 1, 2, 3)', null=True),
        ),
        migrations.AlterField(
            model_name='lead',
            name='requirement',
            field=models.TextField(blank=True, help_text='Requirement details', null=True),
        ),
        migrations.AlterField(
            model_name='lead',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Qualified/Meeting', 'Qualified/Meeting'), ('Proposition', 'Proposition'), ('Completed', 'Completed')], default='New', help_text='Lead status', max_length=20),
        ),
        migrations.AlterField(
            model_name='lead',
            name='win',
            field=models.CharField(choices=[('Win', 'Win'), ('Lost', 'Lost'), ('Awaiting', 'Awaiting')], default='Awaiting', help_text='Win status', max_length=10),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='attendees',
            field=models.TextField(blank=True, help_text='Attendees', null=True),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='duration',
            field=models.DurationField(blank=True, help_text='Duration', null=True),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='end_time',
            field=models.TimeField(blank=True, help_text='End Time', null=True),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='meeting_date',
            field=models.DateField(blank=True, help_text='Meeting Date', null=True),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='meeting_description',
            field=models.TextField(blank=True, help_text='Meeting Description', null=True),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='meeting_title',
            field=models.CharField(blank=True, help_text='Meeting Title', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='meeting_type',
            field=models.CharField(blank=True, choices=[('conference call', 'conference call'), ('in-person', 'in-person'), ('virtual', 'virtual')], help_text='Meeting Type', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='presenters',
            field=models.TextField(blank=True, help_text='Presenter(s)', null=True),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='start_time',
            field=models.TimeField(blank=True, help_text='Start Time', null=True),
        ),
        migrations.CreateModel(
            name='SMS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(blank=True, help_text="Sender's phone number", max_length=100, null=True)),
                ('recipients', models.TextField(blank=True, help_text="Recipient's phone numbers (comma-separated)", null=True)),
                ('message', models.TextField(blank=True, help_text='SMS message content', null=True)),
                ('sent_date_time', models.DateTimeField(auto_now_add=True, help_text='Date and time when the SMS was sent', null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, help_text='Date and time when the profile was created')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date and time when the profile was last updated')),
                ('lead', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sms_details', to='crm_app.lead')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, help_text='Short bio', null=True)),
                ('birth_date', models.DateField(blank=True, help_text='Date of birth', null=True)),
                ('profile_picture', models.ImageField(blank=True, help_text='Profile picture', null=True, upload_to='profile_pictures/')),
                ('phone', models.CharField(blank=True, help_text='Phone number', max_length=15, null=True)),
                ('email', models.EmailField(blank=True, help_text='Email address', max_length=254, null=True)),
                ('address', models.TextField(blank=True, help_text='Address details', null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, help_text='Date and time when the profile was created')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date and time when the profile was last updated')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]