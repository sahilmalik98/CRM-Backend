# Generated by Django 4.2.6 on 2024-08-07 06:35

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0006_meeting_read_receipt_alter_emailattachment_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='leadstatus',
            old_name='updated_at',
            new_name='changed_at',
        ),
        migrations.RemoveField(
            model_name='basicactivityinformation',
            name='status',
        ),
        migrations.RemoveField(
            model_name='emailspecificfields',
            name='sent_date_time',
        ),
        migrations.RemoveField(
            model_name='lead',
            name='win',
        ),
        migrations.RemoveField(
            model_name='leadstatus',
            name='status_from',
        ),
        migrations.RemoveField(
            model_name='leadstatus',
            name='status_to',
        ),
        migrations.RemoveField(
            model_name='meeting',
            name='status',
        ),
        migrations.RemoveField(
            model_name='sms',
            name='sent_date_time',
        ),
        migrations.AddField(
            model_name='leadstatus',
            name='changed_by',
            field=models.CharField(blank=True, help_text='User who changed the status', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='leadstatus',
            name='new_status',
            field=models.CharField(choices=[('New', 'New'), ('Qualified/Meeting', 'Qualified/Meeting'), ('Proposition', 'Proposition'), ('Completed', 'Completed'), ('Win', 'Win'), ('Lost', 'Lost')], default='New', help_text='Current lead status', max_length=20),
        ),
        migrations.AddField(
            model_name='leadstatus',
            name='old_status',
            field=models.CharField(blank=True, choices=[('New', 'New'), ('Qualified/Meeting', 'Qualified/Meeting'), ('Proposition', 'Proposition'), ('Completed', 'Completed'), ('Win', 'Win'), ('Lost', 'Lost')], help_text='Previous lead status', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='lead',
            name='rating',
            field=models.IntegerField(default=1, help_text='Rating (e.g., 1, 2, 3, 4, 5)', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='leadstatus',
            name='lead',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status_changes', to='crm_app.lead'),
        ),
        migrations.CreateModel(
            name='StatusChangeLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_status', models.CharField(blank=True, max_length=20, null=True)),
                ('new_status', models.CharField(blank=True, max_length=20, null=True)),
                ('changed_at', models.DateTimeField(default=django.utils.timezone.now, help_text='Date and time when the status change occurred')),
                ('changed_by', models.CharField(blank=True, help_text='User who changed the status', max_length=255, null=True)),
                ('feedback', models.TextField(blank=True, help_text='Feedback regarding the lead status change', null=True)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status_changes', to='crm_app.basicactivityinformation')),
            ],
        ),
        migrations.CreateModel(
            name='MeetingStatusChangeLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_status', models.CharField(blank=True, help_text='Previous meeting status', max_length=20, null=True)),
                ('new_status', models.CharField(default='Scheduled', help_text='Current meeting status', max_length=20)),
                ('feedback', models.TextField(blank=True, help_text='Feedback regarding the meeting status change', null=True)),
                ('changed_by', models.CharField(blank=True, help_text='User who changed the status', max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date and time when the record was created')),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status_changes', to='crm_app.meeting')),
            ],
        ),
    ]
