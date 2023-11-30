from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser




class User(AbstractUser):
   access_leve = models.CharField(max_length=10, choices=[("NORMAL", "Normal"), ("VIP", "Vip")], default="NORMAL")


class LinkedinUser(models.Model):
   username = models.CharField(max_length=60)
   location = models.CharField(max_length=60)
   skills = models.CharField(max_length=100)
   profile_link = models.URLField()
   profile_image = models.URLField()
   is_completed = models.BooleanField(default=False)

   def __str__(self):
      return self.username


class Experience(models.Model):
   position = models.CharField(max_length=60)
   company = models.CharField(max_length=60)
   date = models.CharField(max_length=60)
   linkedin_user = models.ForeignKey(LinkedinUser, on_delete=models.CASCADE, related_name="experience_user")

   def __str__(self):
      return "%s -- %s" % (self.linkedin_user, self.position)


class Education(models.Model):
   name = models.CharField(max_length=60)
   start_at = models.CharField(max_length=5)
   end_at = models.CharField(max_length=5)
   description = models.CharField(max_length=100)
   linkedin_user = models.ForeignKey(LinkedinUser, on_delete=models.CASCADE, related_name="education_user")

   def __str__(self):
      return "%s -- %s" % (self.linkedin_user, self.name)

