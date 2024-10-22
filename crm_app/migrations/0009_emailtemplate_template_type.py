# Generated by Django 4.2.6 on 2024-10-08 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0008_alter_leadstatus_new_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailtemplate',
            name='template_type',
            field=models.CharField(choices=[('welcome', 'Welcome Email'), ('meeting', 'Meeting Email'), ('notification', 'Notification Email'), ('reminder', 'Reminder Email'), ('template', 'Template')], default='template', help_text='Type of Email Template', max_length=50),
        ),
    ]