from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse

from todo.models import Item

# Create your views here.
def home_page(request):
	if request.method == 'POST':
		Item.objects.create(text = request.POST['new_item'])
		return redirect('/')
	else:
		items = Item.objects.all()
		return render(request, 'home.html', {'items' : items})