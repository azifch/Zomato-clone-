from django.contrib import admin
from .models import Foods,FoodBrands,FoodItems,Restaurants,CartItem,Checkout,Booking
# Register your models here.
class FoodsAdmin(admin.ModelAdmin):
    list_display = ['F_id','F_name','F_dtime','F_rating','F_discount','F_price','F_speciality','F_type','F_image']

class RestaurantsAdmin(admin.ModelAdmin):
    list_display = ['R_id','R_name','R_location','R_distance','R_rating','R_discount','R_price','R_speciality','R_type','R_image']

class FoodBrandsAdmin(admin.ModelAdmin):
    list_display = ['FB_id','FB_name','FB_image','FB_dtime']

class FoodItemsAdmin(admin.ModelAdmin):
    list_display = ['FI_id','FI_name','FI_image']

class CartAdmin(admin.ModelAdmin):
    list_display = ['product','quantity','user']

class CheckoutAdmin(admin.ModelAdmin):
    list_display = ['order_id','quantity','user','is_completed']

class BookingAdmin(admin.ModelAdmin):
    list_display = ['restaurant', 'user','booking_id', 'name', 'email', 'phone_no', 'date', 'time', 'people_size']

admin.site.register(Foods,FoodsAdmin)
admin.site.register(Restaurants,RestaurantsAdmin)
admin.site.register(FoodBrands,FoodBrandsAdmin)
admin.site.register(FoodItems,FoodItemsAdmin)
admin.site.register(Checkout,CheckoutAdmin)
admin.site.register(CartItem,CartAdmin)
admin.site.register(Booking,BookingAdmin)
