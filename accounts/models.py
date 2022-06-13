from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Customuser(AbstractUser):
    is_head = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)
    email = models.EmailField(_('email address'), unique = True)
    dob = models.DateField(max_length=10,null=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    profile_image = models.ImageField(upload_to = 'images/')
    created_on = models.DateTimeField(auto_now_add=True)
    joined_on = models.DateField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name','dob']
    
    def __str__(self):
      return "{}".format(self.email) 



class Vehicle(models.Model):
    id = models.AutoField(primary_key=True)
    vehicle_name = models.CharField(max_length=100)
    vehicle_model = models.CharField(max_length=100)
    vehicle_year = models.CharField(max_length=20)
    type = [
        ('LTV','LTV'),
        ('HTV','HTV')
    ]
    vehicle_type = models.CharField(max_length=4,choices=type,default='LTV')
    vehicle_photo = models.ImageField(upload_to = 'images/')
    chassi_number = models.CharField(max_length=50,unique=True,blank=False)
    registration_number = models.CharField(max_length=40,unique=True,blank=False)

    def __str__(self):
        return self.vehicle_name

class Driver(models.Model):
    user = models.OneToOneField(Customuser,related_name="user",on_delete=models.CASCADE)
    driving_licence = models.ImageField(upload_to='images/')
    licence_expiry_date = models.DateField(max_length=10,null=False)
    vehicle_assigned = models.OneToOneField(Vehicle,on_delete=models.DO_NOTHING)
    address = models.CharField(max_length=200)
    experience = models.CharField(max_length = 2,null=False)
    
    def __str__(self):
        return "{}".format(self.user.email) 


class Manager(models.Model):
    user = models.OneToOneField(Customuser,on_delete=models.CASCADE,related_name='Manager')
    def __str__(self):
        return "{}".format(self.user.email) 
    

class Head(models.Model):
    user = models.OneToOneField(Customuser,on_delete=models.CASCADE,related_name='Head')
    def __str__(self):
        return "{}".format(self.user.email) 