from django.db import models
from django.contrib.auth.models import (BaseUserManager,AbstractBaseUser)

# Create your models here.
from django.db.models import OneToOneField


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
             )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email ,password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin=True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    """
      with this MyUser, trying to create authentication with email and password
    """
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin



class Studentapplication(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    ssc_marks = models.IntegerField()
    internal_marks = models.IntegerField()
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.email

class Department(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.code


class Studentregistration(models.Model):
    studentApplication = models.OneToOneField(Studentapplication, on_delete=models.CASCADE)
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, default=True)
    father_name = models.CharField(max_length=255)
    mobile_no = models.IntegerField()
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='studentimages/')

    def __str__(self):
        return self.studentApplication.email


class Staffregistration(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, default=True)
    name = models.CharField(max_length=255)
    mobile_no = models.IntegerField()
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    exp = models.IntegerField()
    qualification = models.CharField(max_length=255)
    profile_pic = models.ImageField(upload_to='staffimages/')

    def __str__(self):
        return self.user.email

