from django.db import models
from django.urls import reverse
from datetime import date

# Create your models here.

HOURS = (
    ('1', '1 hour'),
    ('2', '2 hours'),
    ('3', '3 hours'),
)
class Guitar(models.Model):
    name = models.CharField(max_length=100)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    description = models.TextField(max_length=250)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'guitar_id': self.id})

class Practice(models.Model):
    date = models.DateField('Last Practice Date')
    hour = models.CharField(
        max_length=1,
        choices=HOURS,
        default=HOURS[0][0]
    )

    guitar = models.ForeignKey(Guitar, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_hour_display()} on {self.date}"

    class Meta:
        ordering = ['-date']
