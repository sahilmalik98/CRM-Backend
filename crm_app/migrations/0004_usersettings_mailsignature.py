# Generated by Django 4.2.16 on 2024-11-18 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0003_contactform'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersettings',
            name='MailSignature',
            field=models.ImageField(blank=True, help_text='Mail Footer', null=True, upload_to='MailSignature/'),
        ),
    ]
