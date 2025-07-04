# Generated by Django 5.2 on 2025-06-23 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='current_class',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='الصف الدراسي'),
        ),
        migrations.AddField(
            model_name='student',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True, verbose_name='تاريخ الميلاد'),
        ),
        migrations.AddField(
            model_name='student',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='student_images/', verbose_name='صورة الطالب'),
        ),
        migrations.AddField(
            model_name='student',
            name='status',
            field=models.CharField(choices=[('New', 'جديد'), ('Existing', 'قديم')], default='New', max_length=10, verbose_name='حالة الطالب'),
        ),
        migrations.AlterField(
            model_name='student',
            name='address',
            field=models.TextField(max_length=100, verbose_name='العنوان'),
        ),
    ]
