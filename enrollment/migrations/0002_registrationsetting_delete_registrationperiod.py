# Generated by Django 5.2 on 2025-06-27 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enrollment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_registration_open', models.BooleanField(default=False, help_text='التحكم العام في فتح أو إغلاق التسجيل للمدرسة بأكملها.', verbose_name='هل التسجيل مفتوح حالياً؟')),
            ],
            options={
                'verbose_name': 'إعداد التسجيل العام',
                'verbose_name_plural': 'إعدادات التسجيل العام',
            },
        ),
        migrations.DeleteModel(
            name='RegistrationPeriod',
        ),
    ]
