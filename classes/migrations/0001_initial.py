# Generated by Django 5.2.1 on 2025-06-17 16:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('academic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاريخ آخر تحديث')),
                ('name', models.CharField(help_text='مثال: الصف الأول - أ، الصف الخامس - ب', max_length=100, verbose_name='اسم الفصل')),
                ('description', models.TextField(blank=True, null=True, verbose_name='الوصف')),
                ('academic_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classes', to='academic.academicyear', verbose_name='العام الدراسي')),
            ],
            options={
                'verbose_name': 'الفصل الدراسي',
                'verbose_name_plural': 'الفصول الدراسية',
                'ordering': ['academic_year__name', 'name'],
                'unique_together': {('academic_year', 'name')},
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاريخ آخر تحديث')),
                ('name', models.CharField(max_length=100, verbose_name='اسم الشعبة')),
                ('stream_type', models.CharField(blank=True, choices=[('Scientific', 'علمي'), ('Literary', 'أدبي'), ('General', 'عام')], help_text='مثل: علمي، أدبي، عام.', max_length=50, null=True, verbose_name='نوع المسار')),
                ('capacity', models.IntegerField(blank=True, help_text='الحد الأقصى لعدد الطلاب في هذا القسم.', null=True, verbose_name='السعة القصوى للقسم')),
                ('is_active', models.BooleanField(default=False, help_text='يشير إلى ما إذا كان القسم قيد الاستخدام حاليًا.', verbose_name='هل القسم نشط؟')),
                ('activation_date', models.DateTimeField(blank=True, null=True, verbose_name='تاريخ التفعيل')),
                ('deactivation_date', models.DateTimeField(blank=True, null=True, verbose_name='تاريخ إلغاء التفعيل')),
                ('academic_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections_by_year', to='academic.academicyear', verbose_name='العام الدراسي')),
                ('class_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='classes.class', verbose_name='الفصل الدراسي')),
            ],
            options={
                'verbose_name': 'القسم',
                'verbose_name_plural': 'الأقسام',
                'ordering': ['academic_year__name', 'class_obj__name', 'name'],
                'unique_together': {('name', 'academic_year', 'class_obj')},
            },
        ),
    ]
