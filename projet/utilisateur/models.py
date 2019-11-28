from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    aliment = models.ManyToManyField("aliment.Aliment")  # int(11) NOT NULL,


#    last_name = models.CharField(max_length=100, blank=True)
#    first_name = models.CharField(max_length=100, blank=True)
#    UserName = models.CharField(max_length=100, blank=True)
#    email = models.CharField(max_length=100, blank=True)
#    password = models.CharField(max_length=100, blank=True)
#
#
#    def _create_user(self, username, email, password, **extra_fields):
#        """
#        Create and save a user with the given username, email, and password.
#        """
#        #if not username:
#        #    raise ValueError('The given username must be set')
#        #email = self.normalize_email(email)
#        ##username = self.model.normalize_username(username)
#        #user = self.model(username=username, email=email, **extra_fields)
#        #user.set_password(password)
#        #user.save(using=self._db)
#        #return user
