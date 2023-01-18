from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users, admin_only
from .models import *
from .forms import OrderForm, RegisterForm, CustomerForm
from .filters import *

# Create your views here.

@login_required(login_url='login')
@admin_only
def home(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()
	total_orders = orders.count()
	orders_delivered = orders.filter(status='Delivered').count()
	orders_pending = orders.filter(status='Pending').count()

	contex = {'orders':orders, 'customers':customers, 'total_orders':total_orders,
	'orders_delivered': orders_delivered, 'orders_pending':orders_pending}
	return render(request, 'dashboard.html', contex)

@unauthenticated_user
def register_page(request):
	form = RegisterForm()
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			messages.success(request, 'Account was Created' + username )

			return redirect('login')

	contex = {'form':form}
	return render(request, 'register.html', contex)

@unauthenticated_user
def login_page(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'username or password was incorrect')

	contex = {}
	return render(request, 'login.html', contex)

@login_required(login_url='login')
def logout_page(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['customers'])
def user_page(request):
	orders = request.user.customer.order_set.all()
	total_orders = orders.count()
	orders_delivered = orders.filter(status='Delivered').count()
	orders_pending = orders.filter(status='Pending').count()

	contex = {'orders':orders, 'total_orders':total_orders,
	'orders_delivered': orders_delivered, 'orders_pending':orders_pending}
	return render(request, 'user.html', contex )


@login_required(login_url='login')
@allowed_users(allowed_roles=['customers'])
def settings(request):
	user = request.user.customer
	form = CustomerForm(instance=user)
	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES, instance=user)
		if form.is_valid:
			form.save()

	contex = {'form':form}
	return render(request, 'account_settings.html', contex)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
	products = Product.objects.all()
	return render(request, 'products.html', {'list':products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customers(request, pk):
	customers = Customer.objects.get(id=pk)
	orders = customers.order_set.all()
	orders_count = orders.count()
	myfilter = OrderFilter(request.GET, queryset=orders)
	orders = myfilter.qs

	contex = {'customers':customers, 'orders':orders, 'orders_count':orders_count,
	'myfilter':myfilter}
	return render(request, 'customers.html',contex)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_order(request, pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product','status'), extra=8)
	customer = Customer.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
	#form = OrderForm(initial={'customer':customer})
	if request.method == 'POST':
		#form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('home')

	contex = {'form':formset, 'customer':customer}
	return render(request, 'order_form.html', contex)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_order(request, pk):
	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)
	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('home')

	contex = {'form':form}
	return render(request, 'order_form.html', contex)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete(request, pk):
	orders = Order.objects.get(id=pk)
	if request.method == 'POST':
		orders.delete()
		return redirect('home')

	contex = {'item':orders}
	return render(request, 'delete.html', contex)