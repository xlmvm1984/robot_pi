# Generated by Django 2.1.3 on 2018-11-20 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise_wechat', '0004_auto_20181118_2225'),
    ]

    operations = [
        migrations.CreateModel(
            name='EnterpriseWechatUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('name', models.CharField(max_length=128)),
                ('mobile', models.CharField(max_length=32)),
                ('gender', models.IntegerField(default=0)),
                ('avatar', models.CharField(max_length=1024)),
            ],
        ),
    ]