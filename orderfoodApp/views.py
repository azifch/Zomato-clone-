import random
from django.db.models import Q
from django.shortcuts import render,redirect,HttpResponse
from .models import Foods,FoodBrands,FoodItems,Restaurants,CartItem,Checkout,Booking,User
from .forms import CreateUserForm
from .forms import BookingForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
import razorpay
# from django_otp.plugins.otp_totp.models import TOTPDevice
# from django_otp.plugins.otp_totp.util import random_hex

# Create your views here.
def index(req):
    return render(req,"index.html")

def items(req):
    food = Foods.objects.all()
    restaurant = Restaurants.objects.all()
    foodbrand = FoodBrands.objects.all()
    fooditem = FoodItems.objects.all()
    context = {'food':food,'foodbrand':foodbrand,'fooditem':fooditem,'restaurant':restaurant}
    return render(req,"items.html",context)

def vegList(req):
    queryset = Foods.prod.veg_list()
    foodbrand = FoodBrands.objects.all()
    fooditem = FoodItems.objects.all()
    context= {'food':queryset,'foodbrand':foodbrand,'fooditem':fooditem}
    return render(req,"items.html",context)

def deliveryTimeList(req):
    queryset = Foods.prod.deliveryTime_list()
    foodbrand = FoodBrands.objects.all()
    fooditem = FoodItems.objects.all()
    context= {'food':queryset,'foodbrand':foodbrand,'fooditem':fooditem}
    return render(req,"items.html",context)

def ratingList(req):
    queryset = Foods.prod.rating_list()
    foodbrand = FoodBrands.objects.all()
    fooditem = FoodItems.objects.all()
    context= {'food':queryset,'foodbrand':foodbrand,'fooditem':fooditem}
    return render(req,"items.html",context)

def itemsDetail(req,fid):
    food = Foods.objects.get(F_id = fid)
    context = {'food':food}
    return render(req,"itemsDetail.html",context)

def search(req):
    query = req.GET.get('q', '')

    # Check if the query matches any restaurants
    if Restaurants.objects.filter(R_name__icontains=query).exists() or Restaurants.objects.filter(R_location__icontains=query).exists():
        action = '/searchRestaurant/'
    else:
        action = '/searchFood/'

    # Perform the appropriate query based on the determined action
    if action == '/searchRestaurant/':
        result = Restaurants.objects.filter(
            Q(R_name__icontains=query) |
            Q(R_location__icontains=query)
        )
        return render(req, "searchRestaurant.html", {'results': result, 'query': query})
    else:
        result = Foods.objects.filter(
            Q(F_name__icontains=query) |
            Q(F_speciality__icontains=query) |
            Q(F_type__icontains=query)
        )
        return render(req, "searchFood.html", {'results': result, 'query': query})

def cart(req):
    if req.user.is_authenticated:
        allproducts = CartItem.objects.filter(user = req.user)
    else:
        return redirect("/login")
    context = {}
    context['cart_items'] = allproducts
    total_price=0
    for x in allproducts:
        total_price += (x.product.F_price * x.quantity)
    context['total'] = total_price
    length = len(allproducts)
    context['items'] = length
    return render(req,"cart.html",context)

def add_cart(req,fid):
    products = Foods.objects.get(F_id = fid)
    user = req.user if req.user.is_authenticated else None
    if user:
        cart_item,created = CartItem.objects.get_or_create(product = products,user=user) 
    else:
        return redirect("/login") 
        # cart_item,created = CartItem.objects.get_or_create(product = products) 
    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1
    cart_item.save()
    return redirect("/cart")

def updateqty(req,uval,fid):
    products = Foods.objects.get(F_id=fid)
    user = req.user
    c = CartItem.objects.filter(product=products,user=user)
    if uval == 1:
        a = c[0].quantity + 1
        c.update(quantity = a)
    else:
        a = c[0].quantity - 1
        c.update(quantity = a)
    return redirect("/cart")

def remove(req,fid):
    m = CartItem.objects.filter(product_id = fid)
    m.delete()
    return redirect("/cart")

def checkout(req):
    c = CartItem.objects.filter(user = req.user)
    context = {}
    context['cart_items'] = c
    total_price=0
    for x in c:
        total_price += (x.product.F_price * x.quantity)
    context['total'] = total_price
    length = len(c)
    context['items'] = length
    return render(req,"checkout.html",context)

def makePayment(req):
    c = CartItem.objects.filter(user = req.user)
    oid = random.randrange(1000,99999)
    for x in c:
        Checkout.objects.create(order_id = oid, product_id = x.product.F_id, user = req.user, quantity = x.quantity)
    orders = Checkout.objects.filter(user = req.user,is_completed=False)
    total_price=0
    for x in orders:
        total_price += (x.product.F_price * x.quantity)
        oid = x.order_id
    client = razorpay.Client(auth=("rzp_test_9r4EOeXGU6gUh9", "1OOx43XwALcea48VsFWTdZ9a"))
    data = {
    "amount": total_price*100,
    "currency": "INR",
    "receipt": "oid",
    }
    payment = client.order.create(data = data)
    context = {}
    context['data'] = payment
    context['amount'] = payment['amount']
    c.delete()
    orders.update(is_completed=True)
    return render(req,"payment.html",context)


def myOrders(req):
    myorder = Checkout.objects.filter(user = req.user,is_completed=True)
    context = {}
    context["myorder"] = myorder
    return render(req,"myorder.html",context)

def restDetail(req,rid):
    restaurant = Restaurants.objects.get(R_id = rid)
    context = {'restaurant':restaurant}
    return render(req,"restDetail.html",context)

def book_table(req):
    R_id = req.POST.get('restaurant')
    id = req.POST.get('user')
    if req.method == 'POST':
        form = BookingForm(req.POST)
        if form.is_valid():
            restaurant_id = req.POST.get('restaurant')
            user_id = req.POST.get('user')
            restaurant = Restaurants.objects.get(R_id=restaurant_id)
            user = User.objects.get(id=user_id)
            form.instance.restaurant = restaurant
            form.instance.user = user
            form.save()
            return redirect("/bookedTable")
    else:
        form = BookingForm()
    return render(req, 'bookTable.html', {'form': form, 'restaurant_id': R_id, 'user_id': id})

def bookedTable(req):
    booked_tables = Booking.objects.all()
    return render(req,"bookedTable.html",{"booked_tables":booked_tables})

def cancelBooking(req,bid):
    booking = Booking.objects.filter(booking_id=bid)
    booking.delete()
    return redirect("/bookedTable")

def register_user(req):
    form = CreateUserForm()
    if req.method == "POST":
        form = CreateUserForm(req.POST)
        if form.is_valid():
            form.save()
            messages.success(req,("User Created Successfully"))
            return redirect("/login")
        else:
            messages.error(req,"Incorrect Password Format")
    context = {'form':form}
    return render(req,"register.html",context)

# def generate_otp_key():
#     return random_hex(20)

# def enable_otp_user(user):
#     otp_key = generate_otp_key()
#     totp_device = TOTPDevice.objects.create(user=user,confirmed=True,key=otp_key)
#     return totp_device

def login_user(req):
    if req.method == 'POST':
        username = req.POST["username"]
        password = req.POST["password"]
        user = authenticate(req,username=username,password=password)
        if user is not None:
            login(req,user)
            messages.success(req,("You have been logged in!!"))
            return redirect("/")
        else:
           messages.error(req,"Incorrect username or Password")
           return redirect("/login") 
    else:
        return render(req,"login.html")
    
def logout_user(req):
    logout(req)
    messages.success(req,("You have logged out Successfully"))
    return redirect("/")
