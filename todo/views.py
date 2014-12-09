from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import date

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

@login_required
def home_page(request):
	items = Item.objects.filter(user=request.user)
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
		print(item.completed_on)
		item.save()
		item = None
		item = Item.objects.get(id=request.POST['item_id'])
		print(item.completed_on)
	return redirect('/home/')

@login_required
def logout_page(request):
	logout(request)
	return redirect('/')