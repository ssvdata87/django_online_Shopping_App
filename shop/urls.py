from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name="home"),
    path('home',views.home,name="home"),
    path('register',views.register,name="register"),
    path('collections',views.collections,name="collections"),
    path('collections/<str:name>/',views.collectionsview,name="collections"),
    path('collections/<str:cname>/,<str:pname>',views.product_details,name="product_details"),
    path('addtocart',views.add_to_cart,name="addtocart"),
    path('ball',views.ball,name="ball"),
    path('g',views.gallery,name="g"),
    path('login',views.login_page,name="login"),
    path('logout',views.logout_page,name="logout"),
    path('cart',views.cart_page,name="cart"),
    path('remove_cart/<str:cid>',views.remove_cart,name="remove_cart"),
    path('fav',views.fav_page,name="fav"),  
    path('favviewpage',views.favviewpage,name="favviewpage"),
    path('orders',views.orders,name="orders"),
    path('remove_fav/<str:fid>',views.remove_fav,name="remove_fav"),
    path('update_cart_quantity',views.update_cart_quantity,name="update_cart_quantity")
]
   