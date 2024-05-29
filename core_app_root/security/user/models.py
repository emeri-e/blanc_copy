from django.db import models

# Create your models here.
from django_countries.fields import CountryField

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
# from django.
import uuid
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
# Create your models here.
import hashlib
class UserManager(BaseUserManager):
    def get_object_by_public_id(self, public_id):
        try:
            instance = self.get(public_id=public_id)
            return instance
        except (ObjectDoesNotExist, ValueError, TypeError):
            return Http404

    def create_user(self, username, email, password=None, **kwargs):
        """Create and return a `User` with an email, phone number, username and password."""
        # if username is None:
        #     raise TypeError('Users must have a username.')
        if email is None:
            raise TypeError('Users must have an email.')
        
        if password is None:
            raise TypeError('User must have an email.')

        user = self.model(username=username, email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password, **kwargs):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')
        if email is None:
            raise TypeError('Superusers must have an email.')
        # if username is None:
        #     raise TypeError('Superusers must have an username.')

        user = self.create_user(username, email, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    public_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4, editable=False)
    username = models.CharField(db_index=True, max_length=255, unique=True,blank=True,null=True)
    first_name = models.CharField(max_length=255,null=True,blank=True)
    last_name = models.CharField(max_length=255,null=True,blank=True)
    # country = CountryField(blank=False,null=True)
    country=models.CharField(max_length=1000,null=True,blank=True)
    # phone_number=models.CharField(max_length=300,blank=True,null=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # Add this line
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    confirm_password=models.CharField(max_length=1000,null=True,blank=True)
    # confirm_password=hashlib.sha256(str(confirm_password).encode()).hexdigest()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    def __str__(self):
        return f"{self.email}"
    def save(self, *args, **kwargs):
        if self.confirm_password:
            self.confirm_password = hashlib.sha256(str(self.confirm_password).encode()).hexdigest()
        super().save(*args, **kwargs)
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
    
    # def __str__(self):
    #     return str(self.full_name)