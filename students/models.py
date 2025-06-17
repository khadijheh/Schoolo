from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User, AutoCreateAndAutoUpdateTimeStampedModel 
from classes.models import Section
from academic.models import AcademicYear

class Student(AutoCreateAndAutoUpdateTimeStampedModel):
    GENDER_CHOICES = [
        ('Male', _('ذكر')),
        ('Female', _('أنثى')),
        ('Other', _('أخرى')), 
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True, 
        related_name='student_profile', 
        verbose_name=_("المستخدم المرتبط")
    )

    section = models.ForeignKey(
        Section, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
        verbose_name=_("القسم")
    )
    enrollment_number = models.CharField(
        max_length=50,
        unique=True,
        null=True, 
        blank=True, 
        verbose_name=_("رقم التسجيل"),
        help_text=_("رقم تسجيل الطالب الفريد في المدرسة. يتم إنشاؤه تلقائياً.")
    )
    father_name = models.CharField(
        max_length=255,
        verbose_name=_("اسم الأب")
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        verbose_name=_("النوع")
    )
    address = models.TextField( 
        verbose_name=_("العنوان")
    )
    parent_phone = models.CharField(
        max_length=20,
        verbose_name=_("رقم هاتف ولي الأمر"),
        help_text=_("رقم هاتف الأب أو الأم للتواصل.")
    )

    class Meta:
        verbose_name = _("الطالب")
        verbose_name_plural = _("الطلاب")
        ordering = ['enrollment_number'] 

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.enrollment_number})"
    
    def save(self, *args, **kwargs):
        if not self.enrollment_number:
            try:
               
                current_academic_year = AcademicYear.objects.get(is_current=True)
                year_prefix = str(current_academic_year.name).split('-')[0] # مثال: '2025-2026' -> '2025'

                # 2. إيجاد آخر رقم تسجيلي للطلاب المسجلين في هذا العام
                # نبحث عن أرقام التسجيل التي تبدأ بـ year_prefix
                last_student = Student.objects.filter(
                    enrollment_number__startswith=f'{year_prefix}-'
                ).order_by('-enrollment_number').first()

                if last_student and last_student.enrollment_number:
                    # استخراج الجزء العددي من رقم التسجيل (مثال: '2025-001' -> '001')
                    last_num_str = last_student.enrollment_number.split('-')[-1]
                    last_num = int(last_num_str)
                    new_num = last_num + 1
                else:
                    new_num = 1 # ابدأ من 1 إذا لم يكن هناك طلاب في هذا العام

                # 3. بناء رقم التسجيل الجديد (مثال: 2025-001، 2025-002، وهكذا)
                # استخدام f-string مع التنسيق لضمان وجود أصفار بادئة (مثال: 001، 010، 100)
                self.enrollment_number = f"{year_prefix}-{new_num:03d}" # 03d تعني 3 أرقام مع أصفار بادئة
                                                                         # يمكنك تعديل 03d إلى 04d إذا كنت تتوقع أكثر من 999 طالبًا في العام

            except AcademicYear.DoesNotExist:
               
                raise Exception(_("لا يوجد عام دراسي حالي نشط لإنشاء رقم تسجيل تلقائي."))
            except Exception as e:
                raise Exception(_(f"فشل في توليد رقم التسجيل التلقائي: {e}"))

        super().save(*args, **kwargs)