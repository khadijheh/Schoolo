from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import AutoCreateAndAutoUpdateTimeStampedModel # استيراد النموذج المساعد
import datetime

class AcademicYear(AutoCreateAndAutoUpdateTimeStampedModel):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("اسم العام الدراسي"),
        help_text=_("مثال: 2024-2025")
    )
    start_date = models.DateField(
        verbose_name=_("تاريخ البدء")
    )
    end_date = models.DateField(
        verbose_name=_("تاريخ الانتهاء")
    )
    is_current = models.BooleanField(
        default=False,
        verbose_name=_("هل هو العام الحالي؟"),
        help_text=_("يجب أن يكون عام دراسي واحد فقط هو الحالي في أي وقت.")
    )

    class Meta:
        verbose_name = _("عام دراسي")
        verbose_name_plural = _("سنوات دراسية")
        ordering = ['-start_date'] 

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_current:
            AcademicYear.objects.filter(is_current=True).exclude(pk=self.pk).update(is_current=False)
        super().save(*args, **kwargs) 


class AcademicTerm(AutoCreateAndAutoUpdateTimeStampedModel):
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.CASCADE,
        related_name='academic_terms', # اسم عكسي للوصول من AcademicYear إلى AcademicTerm
        verbose_name=_("العام الدراسي")
    )
    name = models.CharField(
        max_length=100,
        verbose_name=_("اسم الفصل الدراسي"),
        help_text=_("مثال: الفصل الأول، الفصل الثاني، الفصل الصيفي")
    )
    start_date = models.DateField(
        verbose_name=_("تاريخ البدء")
    )
    end_date = models.DateField(
        verbose_name=_("تاريخ الانتهاء")
    )
    is_current = models.BooleanField(
        default=False,
        verbose_name=_("هل هو الفصل الحالي؟"),
        help_text=_("يجب أن يكون فصل دراسي واحد فقط هو الحالي لكل عام دراسي محدد.")
    )

    class Meta:
        verbose_name = _("فصل دراسي")
        verbose_name_plural = _("فصول دراسية")
        unique_together = [['academic_year', 'name']] # يضمن فرادة اسم الفصل داخل العام الدراسي الواحد
        ordering = ['-academic_year__start_date', 'start_date'] # ترتيب حسب العام ثم تاريخ بدء الفصل

    def __str__(self):
        return f"{self.name} - {self.academic_year.name}"

    def save(self, *args, **kwargs):
        if self.is_current:
            
            AcademicTerm.objects.filter(
                academic_year=self.academic_year, # في نفس العام الدراسي
                is_current=True
            ).exclude(pk=self.pk).update(is_current=False)
        super().save(*args, **kwargs)


