from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from todo.models import Item

def index_page(request):
	if request.user.is_authenticated():
		return redirect('/home/')
	else:
		return redirect('/login/?next=home')

def login_page(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('/home/')
		else:
			return render(request, 'login.html')
	else:
		return render(request, 'login.html')

def signup_page(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password1 = request.POST.get('password1')
		password2 = request.POST.get('password2')
		email = request.POST.get('email')
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		
		errors = list()
		# Check if username is already taken
		try:
			user = User.objects.get(username=username)
			errors.append('Username {} is already taken'.format(username))
		except ObjectDoesNotExist:
			pass
		if not username:
			errors.append('Username cannot be blank')
		if not password1 and not password2:
			errors.append('Password cannot be blank')
		if password1 != password2:
			errors.append('Passwords do not match')
		if not email:
			errors.append('Email address cannot be blank')
		if not first_name:
			errors.append('First name cannot be blank')
		if not last_name:
			errors.append('Last name cannot be blank')

		if not errors:
			User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
			return render(request, 'signup_success.html')
		else:
			return render(request, 'signup.html', {'errors' : errors, 'username':username, 'email':email, 'first_name':first_name, 'last_name':last_name})
	else:
		return render(request, 'signup.html')

@login_required
def home_page(request):
	items = Item.objects.filter(user=request.user) \
		.exclude(Q(cancelled=True) & Q(cancelled_on__lt=date.today())) \
		.exclude(Q(completed=True) & Q(completed_on__lt=date.today()))
	return render(request, 'home.html', {'items' : items})

@login_required
def new_item(request):
	if request.method == 'POST':
		Item.objects.create(text = request.POST['new_item_text'], user=request.user)
	return redirect('/home/')

@login_required
def toggle_complete_item(request):
	if request.method == 'POST':
		item = Item.objects.get(id=request.POST['item_id'])
		item.completed = not item.completed
		item.completed_on = date.today() if item.completed else None
		item.save()
	return redirect('/home/')

@login_required
def cancel_item(request, item_id):
	item = Item.objects.get(id=item_id)
	# make sure user owns the item
	if item.user == request.user:
		item.cancelled = not item.cancelled
		item.cancelled_on = date.today() if item.cancelled else None
		item.completed = False
		item.completed_on = None
		item.save()
	return redirect('/home/')

@login_required
def delete_item(request, item_id):
	item = Item.objects.get(id=item_id)
	# make sure user owns the item
	if item.user == request.user:
		item.delete()
	return redirect('/home/')

@login_required
def logout_page(request):
	logout(request)
	return redirect('/')