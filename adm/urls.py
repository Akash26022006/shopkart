from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name='home'),
    path('register/',register,name = "register2"),
    path('login',login_page,name='login2'),
    path('logout/', logout_page, name='logout'),
    path('collections',collections,name = 'collections'),
    path('collections/<str:name>',collectionsview,name="collections"),
    path('collections/<str:cname>/<str:pname>',product_details,name="product_details"),
    path('addtocart',add_to_cart,name="addtocart"),
    path('fav', add_to_favourite, name='add_to_favourite'),
    path('favourite', favourite_page, name='favourite'),
    path('favourite', favourite_page, name='favourite'),
    path('remove_favourite/<str:fid>', remove_favourite, name='remove_favourite'),
    path('cart',cart_page,name = 'cartpages'),
    path('remove_cart/<str:cid>',remove_cart,name="remove_cart"),
    path('checkout',checkout,name='checkout'),
    path('placeholder',placeholder,name='placeholder'),
    path('buttonholder',buttonholder,name='buttonholder'),
]