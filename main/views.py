from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from . import forms
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart, cartData, guessOrder
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

def registerPage(request):
	form = forms.CreateUserForm()

	if request.method == 'POST':
		form = forms.CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
			user = form.cleaned_data.get('username')
			messages.success(request, 'Account was created for ' + user)
			return redirect('login')

	context = {'form': form}
	return render(request, 'accounts/register.html', context)

def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)
		if user is not None:
			email = user.email
			customer, created = Customer.objects.get_or_create(
				email = email,
			)
			customer.name = user.username
			customer.user = user
			customer.save()
			login(request, user)
			return redirect('store')
		else:
			messages.info(request, 'Username or Password is incorrect')

	context = {}
	return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

def index(request):
	categories = Category.objects.all().order_by('product_category')
	data = cartData(request)
	cartItems = data['cartItems']

	if request.method == 'POST':
		order = request.POST.get('order')
		if order== "Order by name":
			products = Product.objects.all().order_by('name')
		elif order== "Order by price":
			products = Product.objects.all().order_by('price')
	else:
		products = Product.objects.all()
		# messages.add_message(request, messages.WARNING, "not received")
	return render(request, "shop/index.html", locals())

def bycategory(request, category=0):
	categories = Category.objects.all().order_by('product_category')
	data = cartData(request)
	cartItems = data['cartItems']

	if request.method == 'POST':
		order = request.POST.get('order')
		if order== "Order by name":
			products = Product.objects.filter(category=category).order_by('name')
		elif order== "Order by price":
			products = Product.objects.filter(category=category).order_by('price')
	else:
		products = Product.objects.filter(category=category)
		# messages.add_message(request, messages.WARNING, "not received")
	return render(request, "shop/bycategory.html", locals())

def cart(request):
	categories = Category.objects.all().order_by('product_category')
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems': cartItems}
	return render(request, 'shop/cart.html', locals())

def checkout(request):
	categories = Category.objects.all().order_by('product_category')
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems': cartItems}
	return render(request, 'shop/checkout.html', locals())

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)
	elif action == 'delete':
		orderItem.quantity = 0
		orderItem.delete()

	orderItem.save()
	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)

	else:
		customer, order = guessOrder(request,data)

	total = int(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()
	ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment complete', safe=False)

def product_detail(request, beanno=0):
	categories = Category.objects.all().order_by('product_category')
	data = cartData(request)
	cartItems = data['cartItems']

	# if request.user.is_authenticated:
	# 	customer = request.user.customer
	# 	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	# 	items = order.orderitem_set.all()
	# 	cartItems = order.get_cart_items
	# else:
	# 	items=[]
	# 	order = {'get_cart_total':0, 'get_cart_items':0}
	# 	cartItems = order['get_cart_items']

	if beanno==0:
		return redirect('/')
		
	product = Product.objects.get(id=beanno)
	return render(request, "shop/product_detail.html", locals())


def orders(request):
	categories = Category.objects.all().order_by('product_category')
	data = cartData(request)
	cartItems = data['cartItems']
	customer = request.user.customer
	orders = Order.objects.filter(customer=customer)

	return render(request, "shop/user_detail.html", locals())

