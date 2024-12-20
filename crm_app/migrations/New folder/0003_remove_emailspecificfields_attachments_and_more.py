# Generated by Django 4.2.6 on 2024-07-29 05:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0002_remove_emailspecificfields_activity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailspecificfields',
            name='attachments',
        ),
        migrations.RemoveField(
            model_name='lead',
            name='status',
        ),
        migrations.AddField(
            model_name='basicactivityinformation',
            name='feedback',
            field=models.TextField(blank=True, help_text='Feedback regarding the lead status change', null=True),
        ),
        migrations.AddField(
            model_name='emailspecificfields',
            name='feedback',
            field=models.TextField(blank=True, help_text='Feedback regarding the lead status change', null=True),
        ),
        migrations.AddField(
            model_name='meeting',
            name='feedback',
            field=models.TextField(blank=True, help_text='Feedback regarding the lead status change', null=True),
        ),
        migrations.AddField(
            model_name='sms',
            name='feedback',
            field=models.TextField(blank=True, help_text='Feedback regarding the lead status change', null=True),
        ),
        migrations.CreateModel(
            name='LeadStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_from', models.CharField(blank=True, choices=[('New', 'New'), ('Qualified/Meeting', 'Qualified/Meeting'), ('Proposition', 'Proposition'), ('Completed', 'Completed')], help_text='Previous lead status', max_length=20, null=True)),
                ('status_to', models.CharField(choices=[('New', 'New'), ('Qualified/Meeting', 'Qualified/Meeting'), ('Proposition', 'Proposition'), ('Completed', 'Completed')], default='New', help_text='Current lead status', max_length=20)),
                ('feedback', models.TextField(blank=True, help_text='Feedback regarding the lead status change', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date and time when the Status was last updated')),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm_app.lead')),
            ],
        ),
        migrations.CreateModel(
            name='EmailAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, help_text='Attachments', null=True, upload_to='attachments/')),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='email_attachments', to='crm_app.emailspecificfields')),
            ],
        ),
    ]
