from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse, HttpRequest, HttpResponse
import json
import datetime
from django.contrib.auth.models import User
from .utity import cookieCart, cartData, guestOrder
import pickle

# Create your views here.



def index(request):
    data = cartData(request)
    cartItems = data['cartItems']
    
    products = Product.objects.all()
    content ={"products":products,"cartItems":cartItems}
    return render(request,"index.html", content)

def showProduct(request, productId):
    data = cartData(request)
    cartItems = data['cartItems']
    
    product = Product.objects.get(id=productId)
    print(product)
    content = {'product':product, 'cartItems':cartItems }
    return render(request,"showProduct.html",content)

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order'] 
    items = data['items']       
        
    content ={"items":items, 'order':order, 'cartItems':cartItems}
    return render(request,"cart.html", content)

def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order'] 
    items = data['items']

    content = {"items":items, 'order':order, 'cartItems':cartItems}   
    return render(request,"checkout.html", content)



def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('productId:',productId)
    print('action',action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer,complete=False) 
    orderitem, created = OrderItem.objects.get_or_create(order=order,product=product)

    if action == 'add':
        orderitem.quantity += 1
    elif action == 'remove':
        orderitem.quantity -= 1
    orderitem.save()

    if orderitem.quantity <= 0:
        orderitem.delete()

    return JsonResponse('item was added', safe=False)

def orderProcessed(request):
    transection_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    else:
        customer, order = guestOrder(request, data)
        
    total = float(data['form']['total'])
    order.transection_id = transection_id
        
    if total == order.get_cart_total:
        order.complete = True
    order.save()

    ShippingAddress.objects.create(
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        pincode=data['shipping']['pincode'],
        country=data['shipping']['country'],
    )

    # print('Data:', request.body)
    return JsonResponse('item is added',safe=False)


def feedback(request):
    return render(request, 'feedback.html', {})

def about(request):
    return render(request, 'about.html')


def addFeedback(request):
    print(request.body)
    data = json.loads(request.body)
    print(data)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        return customer

    else:
        name = data['userForm']['name'] 
        email = data['userForm']['email']
        # print(name, email)
        customer, created = Customer.objects.get_or_create(            
            email=email,
        )
        customer.name = name
        customer.save()
        return customer
    print(customer.name)
    feedback = Feedback.objects.create(
        customer=customer,
        title=data['feedback']['title'],
        feedback=data['feedback']['feedback'],
    )
    print('feedback:',feedback.customer.name)
    feedback.save()
    print('data', request.body)
    return JsonResponse('feedback  added',safe=False,)


def catagories(request, category):
    data = cartData(request)
    cartItems = data['cartItems']
    catagories ={
        'mobile':1,
        'laptop':2,
        'accesseries':3,
    }
    catagories = Product.objects.filter(catagory_id=catagories[category]) # adding s at the end for looping in html page
    content = {'catagories':catagories, 'cartItems':cartItems}
    return render(request, 'catagory.html', content)