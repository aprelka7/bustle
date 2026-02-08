from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.html import strip_tags
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, first_name, last_name, password=None, **extra_fields):
        if not phone:
            raise ValueError('Поле "телефон" не должно быть пустым')
        user = self.model(phone=phone, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
    

    def create_superuser(self, phone, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(phone, first_name, last_name, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None

    phone = PhoneNumberField(unique=True, max_length=15)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    address1 = models.CharField(max_length=255, blank=True, null=True)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    excluded_allergens = models.ManyToManyField(
        'main.Allergen',
        related_name='users_excluding',
        blank=True,
        verbose_name='исключить аллергены'
    )

    username = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    
    def __str__(self):
        return self.phone
    

    def clean(self):
        for field in ['address1', 'address2', 'city',
                      'country','postal_code', 'phone']:
            value = getattr(self, field)
            if value:
                setattr(self, field, strip_tags(value))