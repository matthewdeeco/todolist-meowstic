from django.db.models import *
from django.contrib.auth.models import User
from django.utils import timezone

class Item(Model):
    text = TextField(default='')
    user = ForeignKey(User, default=None)
    completed = BooleanField(default=False)
    completed_on = DateField(null=True, blank=True)
    created_on = DateTimeField(default=timezone.now())

    def __str__(self):
        return self.text