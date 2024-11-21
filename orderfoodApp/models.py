from django.db import models
from django.contrib.auth.models import User
from django_otp.models import Device

# Create your models here.
class CustomManager(models.Manager):    
    def rating_list(self):
        return self.filter(F_rating__gte = "4.0")
    
    def veg_list(self):
        return self.filter(F_type__exact = "Veg")
    
    def deliveryTime_list(self):
        return super().get_queryset().order_by("F_dtime")
    

class FoodItems(models.Model):
    FI_id = models.IntegerField(primary_key=True)
    FI_name = models.CharField(max_length=25)
    FI_image = models.ImageField(upload_to="pics")


class FoodBrands(models.Model):
    FB_id = models.IntegerField(primary_key=True)
    FB_name = models.CharField(max_length=25)
    FB_dtime = models.CharField(max_length=25)
    FB_image = models.ImageField(upload_to="pics")

class Foods(models.Model):
    F_id = models.IntegerField(primary_key=True)
    F_name = models.CharField(max_length=25)
    F_dtime = models.CharField(max_length=25)
    F_rating = models.CharField(max_length=25)
    F_discount = models.CharField(max_length=25)
    F_price = models.IntegerField()
    F_speciality = models.CharField(max_length=50)
    F_type = models.CharField(max_length=50,choices=(('Veg','Veg'),('Non-Veg','Non-Veg')),default="Veg")
    F_image = models.ImageField(upload_to="pics")

    prod = CustomManager()
    objects=models.Manager()

class Restaurants(models.Model):
    R_id = models.IntegerField(primary_key=True)
    R_name = models.CharField(max_length=25)
    R_location = models.CharField(max_length=50,default=0)
    R_distance = models.CharField(max_length=25)
    R_rating = models.CharField(max_length=25)
    R_discount = models.CharField(max_length=25)
    R_price = models.IntegerField()
    R_speciality = models.CharField(max_length=50)
    R_type = models.CharField(max_length=50,choices=(('Veg','Veg'),('Non-Veg','Non-Veg')),default="Veg")
    R_image = models.ImageField(upload_to="pics")

class Booking(models.Model):
    restaurant = models.ForeignKey(Restaurants,on_delete = models.CASCADE,default=0)
    user = models.ForeignKey(User,on_delete = models.CASCADE,default=0)
    booking_id = models.IntegerField(primary_key=True,default=0)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_no = models.CharField(max_length=12)
    date = models.DateField()
    time = models.TimeField()
    people_size = models.IntegerField()

class CartItem(models.Model):
    product = models.ForeignKey(Foods,on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add = True)
    user = models.ForeignKey(User,on_delete = models.CASCADE, default=1)

class Checkout(models.Model):
    order_id = models.IntegerField()
    product = models.ForeignKey(Foods,on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add = True)
    user = models.ForeignKey(User,on_delete = models.CASCADE, default=1)
    is_completed = models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class UserOTPDevice(Device):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)