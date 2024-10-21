from django.shortcuts import render
from .models import *
from . utils import cookieCart, cartData, guestOrder
from django.http import JsonResponse
import json
import datetime
# Create your views here.

def my_view(request):
    response = JsonResponse({"data": "your_data"})
    response['Access-Control-Allow-Origin'] = '*'
    return response

def store(request):
  data = cartData(request)
  cartItems = data['cartItems']

  products = Product.objects.all()
  #  a dictionary named context is created, which will be passed to the template. The key is "products" and its value is the QuerySet of products retrieved in the previous step.
  context = {"products":products, "cartItems":cartItems}
  # combines the request, the specified template, and the context dictionary
  return render(request, 'store/store.html', context)

def cart(request):
  data = cartData(request)
  cartItems = data['cartItems']
  order = data['order']
  items = data['items']

  context = {"items":items, "order":order, "cartItems":cartItems}
  return render(request, 'store/cart.html', context)

def checkout(request):
  
  data = cartData(request)
  cartItems = data['cartItems']
  order = data['order']
  items = data['items']
    
  context = {"items":items, "order":order, "cartItems":cartItems}
  return render(request, 'store/checkout.html',context)

def updateItem(request):
  data = json.loads(request.body)
  productId = data['productId']
  action = data['action']

  print('Action:',action)
  print('Product:',productId)

  if request.user.is_authenticated:
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
      orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
      orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
      orderItem.delete()

  else:
      return JsonResponse('User is not authenticated', safe=False)
  
  return JsonResponse("Item was added", safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    # Correct total comparison
    if total == float(order.get_cart_total()):
        order.complete = True

    else:
        print("Total mismatch: Order total:", order.get_cart_total, "Paid total:", total)

    order.save()

    if order.shipping:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment complete!', safe=False)
