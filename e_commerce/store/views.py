from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required
from . models import *
from django.http import JsonResponse
import json
import datetime
from .forms import RegisterForm
from django.contrib.auth import login


# def store(request):
# 	context = {}
# 	return render(request, 'store/store.html', context)




def cart(request):
	if request.user.is_authenticated:
		customer= request.user.customer
		order,created=Order.objects.get_or_create(customer=customer,complete=False)
		items= order.orderitem_set.all()
		cartItems=order.get_cart_items
	else:
		items=[]
		order={'get_cart_total':0,'get_cart_items':0}
		cartItems = order['get_cart_items']
	
	context={'items':items,'order':order,'cartItems':cartItems}
	return render(request, 'store/cart.html', context)





def checkout(request):
	if request.user.is_authenticated:
		customer=Customer.objects.filter(user=request.user).first()
		# customer=request.user.customer
		order,created=Order.objects.get_or_create(customer=customer,complete=False)
		items=order.orderitem_set.all()
		cartItems=order.get_cart_items
	else:
		customer=       customer = Customer.objects.create(user=request.user, name=request.user.username, email=request.user.email)
		items=[]
		order={'get_cart_tptal':0,'get_cart_items':0}
		cartItems=order['get_cart_items']
	
	context={'items':items,'order':order,'cartItems':cartItems}

	return render(request, 'store/checkout.html', context)





def store(request):
	if request.user.is_authenticated:
		try:
			customer= request.user.customer
		except Customer.DoesNotExist:
			 customer = Customer.objects.create(user=request.user, name=request.user.username, email=request.user.email)
        

		order,created=Order.objects.get_or_create(customer=customer,complete=False)
		items= order.orderitem_set.all()
		cartItems=order.get_cart_items
	else:
		items=[]
		order={'get_cart_total':0,'get_cart_items':0}
		cartItems=order['get_cart_items']
	products=Product.objects.all()
	context={'products':products,'cartItems':cartItems}
	return render(request,'store/store.html',context)



def updateItem(request):
	data=json.loads(request.body)
	productId=data['productId']
	action=data['action']
	print(action)
	print(productId)

	customer=request.user.customer
	product=Product.objects.get(id=productId)
	order,created=Order.objects.get_or_create(customer=customer,complete=False)
	orderItem,created=OrderItem.objects.get_or_create(order=order,product=product)

	if action=='add':
		orderItem.quantity+=1
	elif action=='remove':
		orderItem.quantity-=1
	
	orderItem.save()

	if orderItem.quantity<=0:
		orderItem.delete()

	return JsonResponse('Item was added',safe=False)


@login_required
def processOrder(request):
	transaction_id=datetime.datetime.now().timestamp()
	data=json.loads(request.body)


	if request.user.is_authenticated:
		customer=request.user.customer
		order,created=Order.objects.get_or_create(customer=customer,complete=False)
		total=float(data['form']['total'])
		order.transaction_id=transaction_id

		if total==order.get_cart_total:
			order.complete=True
			order.save()

		if order.shipping==True:
			ShippingAddress.objects.create(customer=customer,
																	order=order,
																	address=data['shipping']['address'],
																	city=data['shipping']['city'],
																	state=data['shipping']['state'],
																	zipcode=data['shipping']['zipcode'],)
	else:
		print("User is not logged in")

	return JsonResponse('Payment sumbitted')


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Create the user
            # Create the customer instance for the user
            customer = Customer.objects.create(user=user, name=user.username, email=user.email)
            # Login the user after registration
            login(request, user)
            return redirect('store')
    else:
        form = RegisterForm()

    return render(request, 'store/registration/register.html', {'form': form})