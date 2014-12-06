from django.db.models import *
from django.contrib.auth.models import User 

class Item(Model):
	text = TextField(default='')
	user = ForeignKey(User, default=None)