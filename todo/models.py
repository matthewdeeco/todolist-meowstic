from django.db.models import *

# Create your models here.
class Item(Model):
	text = TextField(default='')