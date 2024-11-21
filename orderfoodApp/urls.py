from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('items/', views.items, name='items'),
    path('restDetail/<int:rid>', views.restDetail, name='restDetail'),
    path('itemsDetail/<int:fid>', views.itemsDetail, name='itemsDetail'),
    path('cart/', views.cart, name='cart'),
    path('search/', views.search, name='search'),
    path('addcart/<int:fid>', views.add_cart, name='addcart'),
    path('updateqty/<int:uval>/<int:fid>',views.updateqty,name='updateqty'),
    path('remove/<int:fid>', views.remove, name='remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('makePayment/', views.makePayment, name='makePayment'),
    path('myOrders/', views.myOrders, name='myOrders'),
    path('book_table/', views.book_table, name='book_table'),
    path('bookedTable/', views.bookedTable, name='bookedTable'),
    path('cancelBooking/<int:bid>/', views.cancelBooking, name='cancelBooking'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('ratingList/', views.ratingList, name='ratingList'),
    path('vegList/', views.vegList, name='vegList'),
    path('deliveryTimeList/', views.deliveryTimeList, name='deliveryTimeList'),
]