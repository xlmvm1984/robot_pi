# Generated by Django 2.1.3 on 2018-11-18 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise_wechat', '0003_enterprisewechatapp_remark'),
    ]

    operations = [
        migrations.AddField(
            model_name='enterprisewechatapp',
            name='message_aes_key',
            field=models.CharField(default='', max_length=1024),
        ),
        migrations.AddField(
            model_name='enterprisewechatapp',
            name='message_callback_url',
            field=models.CharField(default='', max_length=1024),
        ),
        migrations.AddField(
            model_name='enterprisewechatapp',
            name='message_token',
            field=models.CharField(default='', max_length=1024),
        ),
    ]