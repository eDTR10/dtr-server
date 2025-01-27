from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from department.models import Department

class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

    def get_by_natural_key(self, email):
        return self.get(email=email)

class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    uid = models.IntegerField(unique=True, primary_key=True)
    card = models.IntegerField(default=0)
    access_lvl = models.IntegerField(default=3)

    # New fields
    sex = models.CharField(max_length=8, null=True, blank=True)
    job_title = models.CharField(max_length=100, null=True, blank=True)
    email2 = models.CharField(max_length=100, null=True, blank=True)
    birthday = models.DateTimeField(null=True, blank=True)
    hiredday = models.DateTimeField(null=True, blank=True)
    street = models.CharField(max_length=80, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True)
    zip = models.CharField(max_length=12, null=True, blank=True)
    ophone = models.CharField(max_length=20, null=True, blank=True)
    deptid = models.ForeignKey(Department, on_delete=models.CASCADE, to_field='deptid') 
    photos = models.ImageField(upload_to='photos/', null=True, blank=True)
    status = models.SmallIntegerField(default=1)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'uid','access_lvl']

    def get_full_name(self):
        return self.full_name
