from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json
import datetime

from django.http import JsonResponse
from .utils import cartData , guestOrder

# Create your views here.


def store(request):
     data = cartData(request)
     cartsItems = data['cartItems']

     products = Product.objects.all()
     context = {'products' : products , 'cartsItems' : cartsItems }
     return render(request, 'store/store.html', context)


def cart(request):
     data = cartData(request)
     order = data['order']
     cartsItems = data['cartItems']
     items = data['items']

     context = {'items' : items , 'order' : order , 'cartsItems' : cartsItems}
     return render(request, 'store/cart.html', context)

 
def checkout(request):
     data = cartData(request)
     order = data['order']
     cartsItems = data['cartItems']
     items = data['items']
     

     context = {'items' : items , 'order' : order , 'cartsItems' : cartsItems }
     return render(request, 'store/checkout.html', context)


def uptdateItem(request):
     data = json.loads(request.body)
     productId = data['productId']
     action = data['action']

     customer = request.user.customer

     product = Product.objects.get(id=productId)
     order , created = Order.objects.get_or_create(customer = customer , complete = False)
     
     orderItem , created = OrderItem.objects.get_or_create(order=order , product = product)

     if action == 'add':
          orderItem.quantity = (orderItem.quantity + 1)
     elif action == "remove":
          orderItem.quantity = (orderItem.quantity - 1)

     orderItem.save()

     if orderItem .quantity <= 0:
          orderItem.delete()

     return JsonResponse('Item was added' , safe=False)


@csrf_exempt
def processOrder(request):
     try:
          data = json.loads(request.body)

          transactionId = datetime.datetime.now().timestamp()

          if request.user.is_authenticated:
               customer = request.user.customer
               order , created = Order.objects.get_or_create(customer = customer , complete = False)

          else:
               customer , order = guestOrder(request , data)

          total = float(data['form']['total'])
          order.transaction_id = transactionId
               
          if total == float(order.get_cart_total):
               order.complete = True
               
          order.save()
          if order.shipping == True:
               ShippingAddress.objects.create(
                    customer = customer,
                    order = order,
                    address = data['shipping']['address'],
                    city = data['shipping']['city'],
                    state = data['shipping']['state'],
                    zipcode = data['shipping']['zipcode'],
               )
               
          return JsonResponse('Payment submitted...' , safe=False)
     except :
          return JsonResponse({'error': 'Malformed JSON data in request body.'}, status=400)


#      try:
#         data = json.loads(request.body)
#     except json.JSONDecodeError:

     
