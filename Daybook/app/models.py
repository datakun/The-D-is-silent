from datetime import datetime
from django.utils import timezone
from django.db import models
import pytz


class Daybooks(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    user_id = models.CharField(max_length=20)
    date_format = models.CharField(max_length=8)
    date = models.DateTimeField()
    weather = models.TextField(max_length=100)
    title = models.TextField(max_length=100)
    content = models.TextField()

    def get_time_difference(self, date_time=None):
        if date_time is None:
            if self.date:
                now = datetime.now()
                timediff = datetime(now.year, now.month, now.day) - datetime(self.date.year,
                                                                             self.date.month,
                                                                             self.date.day)

                return timediff.days
        else:
            if self.date:
                timediff = datetime(date_time.year, date_time.month, date_time.day) - datetime(
                    self.date.year, self.date.month, self.date.day)

                return timediff.days

    def get_date_value(self):
        if self.date:
            return self.date.strftime('%Y/%m/%d')

    def get_date_value_tag(self):
        if self.date:
            return self.date.strftime('%Y%m%d')