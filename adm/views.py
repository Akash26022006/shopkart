from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
import random
from django.http import  JsonResponse
import json
 
from django.contrib.auth import authenticate,login,logout

# Create your views here.
# authorization

def index(request):
    products=Product.objects.filter(trending=1)
    print('products',products)
    category=Category.objects.filter(status=0)
    print(products)
    return render(request,"pages/index.html",{"products":products,"categories" : category})

def logout_page(request):
  if request.user.is_authenticated:
    logout(request)
    messages.success(request,"Logged out Successfully")
  return redirect("home")
 
 
def login_page(request):
  if request.user.is_authenticated:
    return redirect("/")
  else:
    if request.method=='POST':
    #   name=request.POST['username']
    #   pwd=request.POST.get('password')
      user=authenticate(request,username=request.POST['username'],
                        password=request.POST['password'])
      if user is not None:
        login(request,user)
        messages.success(request,"Logged in Successfully")
        return redirect("/")
      else:
        messages.error(request,"Invalid User Name or Password")
        return redirect("/login")
    return render(request,"pages/login.html")
 
def register(request):
  print("request")
  if request.method == 'POST':
    print("request",request.POST)
    User.objects.create_user(
                  username=request.POST['username'],
                  email=request.POST.get('email'),
                  password=request.POST['password']  # Django will hash this automatically
              )
    messages.success(request,"Registration Success You can Login Now..!")
    return redirect('/login')
  return render(request,"pages/register.html")


def collections(request):
  print(5)
  category=Category.objects.filter(status=0)
  return render(request,"pages/collections.html",{"category":category})

def collectionsview(request,name):
  print(5555)
  print(name)
  if(Category.objects.filter(name=name,status=0)):
      # products=Product.objects.filter(category__name=name)
   
      category = Category.objects.filter(name = name).first()
      products=Product.objects.filter(category_id = category.id)
      # print(products,'products')
      return render(request,"products/index.html",{"products":products,"category_name":name})
  else:
    messages.warning(request,"No Such Catagory Found")
    return redirect('collections')
  
def product_details(request,cname,pname):
    if(Category.objects.filter(name=cname,status=0)):
      if(Product.objects.filter(name=pname,status=0)):
        products=Product.objects.filter(name=pname,status=0).first()
        print(products)
        return render(request,"products/productdetails.html",{"products":products})
      else:
        messages.error(request,"No Such Produtct Found")
        return ("/")
    messages.error(request,"No Such Catagory Found")
    return redirect('collections')

def add_to_cart(request):
      if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
          data=json.load(request)
          # data = {"product_qty" : 5,pid:1}
          product_qty=data['product_qty'] #5
          product_id=data['pid']
          #print(request.user.id)
          product_status=Product.objects.filter(id=product_id).first()
          if product_status:
            if Cart.objects.filter(user_id = request.user.id,product_id=product_id):
              return JsonResponse({'status':'Product Already in Cart'}, status=200)
            else:
              if product_status.quantity>=product_qty:
                cart = Cart(user_id =request.user.id,product_id=product_id,product_qty=product_qty)
                cart.save()
                
                
                return JsonResponse({'status':'Product Added to Cart'}, status=200)
              else:
                return JsonResponse({'status':'Product Stock Not Available'}, status=200)
        else:
          return JsonResponse({'status':'Login to Add Cart'}, status=200)
      else:
        return JsonResponse({'status':'Invalid Access'}, status=200)

def add_to_favourite(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        if request.user.is_authenticated:

            data = json.load(request)
            product_id = data['pid']

            product = Product.objects.filter(id=product_id).first()

            if product:
                if Favourite.objects.filter(
                    user_id=request.user.id,
                    product_id=product_id
                ).exists():

                    return JsonResponse({
                        'status': 'Product Already in Favourite'
                    }, status=200)

                Favourite.objects.create(
                    user_id=request.user.id,
                    product_id=product_id
                )

                return JsonResponse({
                    'status': 'Product Added to Favourite'
                }, status=200)

            return JsonResponse({
                'status': 'Product Not Found'
            }, status=200)

        return JsonResponse({
            'status': 'Login to Add Favourite'
        }, status=200)

    return JsonResponse({
        'status': 'Invalid Access'
    }, status=200)


def favourite_page(request):

    if request.user.is_authenticated:

        favourite = Favourite.objects.filter(
            user_id=request.user.id
        )

        return render(
            request,
            "pages/favourite.html",
            {"favourite": favourite}
        )

    return redirect("/")

      

def cart_page(request):
  if request.user.is_authenticated:
    # cart=Cart.objects.filter(user_id=request.user.id).values()

    cart=Cart.objects.filter(user_id=request.user.id)
    # for item in cart:
    #   print('item',item)
    #   price = Product.objects.filter(id = item['product_id']).first()
    #   item['total_price'] = price.selling_price*item['product_qty']
 
    return render(request,"pages/cart.html",{"cart":cart})
  else:
    return redirect("/")
  
def remove_cart(request,cid):
  cartitem=Cart.objects.get(id=cid)
  cartitem.delete()
  return redirect("/cart")

def checkout(request):
  if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request,"pages/checkout.html",{"carts":cart})
  else:
    return redirect("/")
  
def placeholder(request):
      if request.user.is_authenticated:
            if request.method=="POST" :
                  neworder = Order()
                  neworder.user = request.user
                  neworder.fname = request.POST.get('fname')
                  neworder.lname = request.POST.get('lname')
                  neworder.email = request.POST.get('email')
                  neworder.phone = request.POST.get('phone')
                  neworder.address = request.POST.get('address')
                  neworder.city = request.POST.get('city')
                  neworder.state = request.POST.get('state')
                  neworder.country = request.POST.get('country')
                  neworder.pincode = request.POST.get('pincode')
                  neworder.payment_mode = request.POST.get('payment_mode')
                  neworder.total_price = request.POST.get('total_price')
                  
                 
              
                  carts = Cart.objects.filter(user=request.user)
                  cart_total_price = 0
                  for item in carts:
                         cart_total_price = cart_total_price + item.product.selling_price * item.product_qty
                         neworder.product=item.product.name,

                  neworder.total_price= cart_total_price
                  trackno = 'maddyshopkart' + str(random.randint(1111111,9999999))
                  while Order.objects.filter(tracking_no=trackno) is None:
                        trackno = 'maddyshopkart'+str(random.randint(1111111,9999999))

                  neworder.tracking_no  = trackno
                  neworder.save()

                  """neworderitems = Cart.objects.filter(user=request.user)
                  for item in neworderitems:
                        OrderItem.objects.create(
                          order=neworder,
                          product=item.product.name,
                          price=item.product.selling_price,
                          quantity=item.product_qty
                    )

                        orderproduct = Product.objects.filter(id=item.product_id).first()
                        orderproduct.quantity = orderproduct.quantity - item.product_qty
                        orderproduct.save()"""
              
                  Cart.objects.filter(user=request.user).delete()
                  messages.success(request,"Your order has been placed successfully")
          
      else:
            return render('/')
           
      return render(request,"pages/thanks.html")


def remove_favourite(request, fid):
    if request.user.is_authenticated:
        favourite = Favourite.objects.filter(
            id=fid,
            user_id=request.user.id
        ).first()

        if favourite:
            favourite.delete()
            messages.success(request, "Removed from Favourite")

        return redirect('favourite')

    return redirect('home')
 
            
           
def buttonholder(request):
      print("buttonholder")
      if request.user.is_authenticated:
            print("authenticate")
            if request.method=="POST" :
                  neworder = Order()
                  #neworder.user = request.user
                  neworder.user = request.user
                  neworder.fname = request.POST.get('fname')
                  neworder.lname = request.POST.get('lname')
                  neworder.email = request.POST.get('email')
                  neworder.phone = request.POST.get('phone')
                  neworder.address = request.POST.get('address')
                  neworder.city = request.POST.get('city')
                  neworder.state = request.POST.get('state')
                  neworder.country = request.POST.get('country')
                  neworder.pincode = request.POST.get('pincode')
                  neworder.payment_mode = request.POST.get('payment_mode')
                  neworder.total_price = request.POST.get('total_price')
                  neworder.save()
                  messages.success(request,"Your order has been placed successfully")  
      else:
            print("no")
            return render(request,'products/buynow.html')       
      return render(request,"pages/thanks.html")
