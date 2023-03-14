# ///File: store/urls.py
from django.urls import path

from . import views

urlpatterns = [
        #Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    
    path('uptade_item/' , views.uptdateItem , name="update_item"),
    path('process_order/' , views.processOrder , name="process_order")

]