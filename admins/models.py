from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User, AutoCreateAndAutoUpdateTimeStampedModel

class Admin(AutoCreateAndAutoUpdateTimeStampedModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True, 
        related_name='admin_profile', 
        verbose_name=_("المستخدم المرتبط")
    )
    department = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("القسم")
    )

    class Meta:
        verbose_name = _("المسؤول")
        verbose_name_plural = _("المسؤولون")
        ordering = ['user__first_name', 'user__last_name'] # ترتيب المسؤولين بالاسم

    def __str__(self):
        return self.user.get_full_name() or self.user.phone_number
    
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='accounts_user_set', # <-- أضف هذا الاسم الفريد
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='accounts_user_permissions_set', # <-- أضف هذا الاسم الفريد
        related_query_name='user',
    )

    def __str__(self):
        return self.username