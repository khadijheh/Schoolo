from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

class AutoCreateAndAutoUpdateTimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاريخ الإنشاء"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("تاريخ آخر تحديث"))

    class Meta:
        abstract = True

class UserManager(BaseUserManager):
    def _create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError(_('The Phone Number must be set'))
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_student_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', False) 
        return self._create_user(phone_number, password, **extra_fields)

    def create_teacher_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False) 
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', False) 
        return self._create_user(phone_number, password, **extra_fields)

    def create_admin_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', False) 
        return self._create_user(phone_number, password, **extra_fields)
    
    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self._create_user(phone_number, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin , AutoCreateAndAutoUpdateTimeStampedModel):
    phone_number = models.CharField(max_length=10, unique=True, verbose_name=_('رقم الهاتف'))
    first_name = models.CharField(max_length=150, blank=True, verbose_name=_('الاسم الأول'))
    last_name = models.CharField(max_length=150, blank=True, verbose_name=_('الاسم الأخير')) 
    is_active = models.BooleanField(default=False, verbose_name=_('نشط')) 
    is_staff = models.BooleanField(default=False, verbose_name=_('موظف'))
    is_superuser = models.BooleanField(default=False, verbose_name=_('مشرف'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاريخ الإنشاء'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('تاريخ آخر تحديث'))
    last_login = models.DateTimeField(null=True, blank=True, verbose_name=_('آخر تسجيل دخول')) # أضفتها من AbstractUser

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = [] # يمكنك إضافة 'first_name', 'last_name' هنا إذا أردتها مطلوبة عند create_superuser

    class Meta:
        verbose_name = _('المستخدم')
        verbose_name_plural = _('المستخدمون')

    def __str__(self):
        return self.phone_number

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name