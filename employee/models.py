from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
# Create your models here.

class Group(models.Model):
    name_group = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name_group)

class Role(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return str(self.title)
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='name')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)
    group = models.ForeignKey(Group , on_delete=models.CASCADE,null=True)
    sex = models.BooleanField()
    ethnicity = models.CharField(max_length=100)
    earnings = models.IntegerField()
    date_of_birth = models.DateField()
    join_date = models.DateField()
    full_time = models.BooleanField()
    location = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatar', blank=True, null=True, max_length=2000)
    phone = models.CharField(max_length=100,null=True, blank=True)
    slug = models.SlugField(max_length=2000, null=False)

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.user.username)
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.user.username)

class SocailMedia(models.Model):
    name = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    facebook = models.CharField(max_length=100,null=True, blank=True)
    twitter = models.CharField(max_length=100, null=True, blank=True)
    linkedin = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return str(self.name)


class Payroll(models.Model):
    name = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    salary = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return str(self.date)

