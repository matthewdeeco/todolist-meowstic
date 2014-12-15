from django.db.models import *
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date
import calendar

class DailyItemManager(Manager):
    def get_queryset(self):
        today = date.today()
        return super(DailyItemManager, self).get_queryset() \
            .filter(due_on__lte=today) \
            .exclude((Q(cancelled=True) | Q(completed=True)) & Q(marked_on__lt=today))

class WeeklyItemManager(Manager):
    def get_queryset(self):
        Saturday = 5
        today = date.today()
        days_till_upcoming_saturday = (Saturday - today.weekday()) % 7
        upcoming_saturday = date.fromordinal(today.toordinal() + days_till_upcoming_saturday)
        return super(WeeklyItemManager, self).get_queryset() \
            .filter(due_on__lte=upcoming_saturday) \
            .exclude((Q(cancelled=True) | Q(completed=True)) & Q(marked_on__lt=today))

class MonthlyItemManager(Manager):
    def get_queryset(self):
        today = date.today()
        days_in_month = calendar.monthrange(today.year, today.month)[1]
        end_of_month = today.replace(day=days_in_month)

        return super(MonthlyItemManager, self).get_queryset() \
            .filter(due_on__lte=end_of_month) \
            .exclude((Q(cancelled=True) | Q(completed=True)) & Q(marked_on__lt=today))

class Item(Model):
    text = TextField(default='')
    user = ForeignKey(User, default=None)
    due_on = DateField(default=date.today())

    completed = BooleanField(default=False)
    cancelled = BooleanField(default=False)
    marked_on = DateField(null=True, blank=True)
    created_on = DateTimeField(default=timezone.now())

    objects = Manager()
    daily_objects = DailyItemManager()
    weekly_objects = WeeklyItemManager()
    monthly_objects = MonthlyItemManager()

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
