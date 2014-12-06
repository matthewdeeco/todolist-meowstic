from django.db.models import *

class Item(Model):
	text = TextField(default='')