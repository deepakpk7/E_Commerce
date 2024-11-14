from django.urls import path
from . import views


urlpatterns = [
    path('',views.e_shop_login),
    path('register',views.register),
    path('shop_home',views.shop_home),
    path('add_pro',views.add_product),
    path('logout',views.e_shop_logout),
    
]