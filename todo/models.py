from django.db.models import *
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date

class Item(Model):
    text = TextField(default='')
    user = ForeignKey(User, default=None)
    due_on = DateField(default=date.today())

    completed = BooleanField(default=False)
    cancelled = BooleanField(default=False)
    marked_on = DateField(null=True, blank=True)
    created_on = DateTimeField(default=timezone.now())

    def __str__(self):
        return self.text

    def due(self):
        return self.due_on == date.today()

    def overdue(self):
        return self.due_on < date.today()

    def due_in(self):
        return self.due_on.toordinal() - date.today().toordinal()

    def overdue_by(self):
        return date.today().toordinal() - self.due_on.toordinal()