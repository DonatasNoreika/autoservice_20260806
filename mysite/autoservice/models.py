from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="profile_pics", null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo:
            img = Image.open(self.photo.path)
            min_side = min(img.width, img.height)
            left = (img.width - min_side) // 2
            top = (img.height - min_side) // 2
            right = left + min_side
            bottom = top + min_side
            img = img.crop((left, top, right, bottom))
            img = img.resize((300, 300), Image.LANCZOS)
            img.save(self.photo.path)

    def __str__(self):
        return f"{self.user.username} profile"


class Service(models.Model):
    name = models.CharField()
    price = models.IntegerField()

    def __str__(self):
        return self.name


class Car(models.Model):
    make = models.CharField()
    model = models.CharField()
    license_plate = models.CharField(max_length=10)
    vin_code = models.CharField(max_length=17)
    client_name = models.CharField()
    photo = models.ImageField(upload_to='cars', null=True, blank=True)
    description = HTMLField(default="")

    def __str__(self):
        return f"{self.make} {self.model}"


class Order(models.Model):
    car = models.ForeignKey(to="Car",
                            on_delete=models.SET_NULL,
                            null=True, blank=True,
                            related_name="orders")
    date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True)

    LOAN_STATUS = (
        ('p', 'Patvirtinta'),
        ('v', 'Vykdoma'),
        ('i', 'Įvykdyta'),
        ('a', 'Atmesta'),
    )

    status = models.CharField(choices=LOAN_STATUS, default='p')
    client = models.ForeignKey(to=User,
                               on_delete=models.SET_NULL,
                               null=True, blank=True)

    def total(self):
        result = 0
        for line in self.lines.all():
            result += line.service.price * line.quantity
        return result

    def is_overdue(self):
        return self.deadline and timezone.now() > self.deadline

    def __str__(self):
        return f"{self.car} ({self.date})"

    class Meta:
        ordering = ['-pk']


class OrderLine(models.Model):
    order = models.ForeignKey(to="Order",
                              on_delete=models.CASCADE,
                              related_name="lines")
    service = models.ForeignKey(to="Service",
                                on_delete=models.SET_NULL,
                                null=True, blank=True)
    quantity = models.IntegerField(default=1)

    def line_sum(self):
        return self.service.price * self.quantity

    def service_price(self):
        return self.service.price

    def __str__(self):
        return f"{self.service} - {self.quantity}"


class OrderComment(models.Model):
    order = models.ForeignKey(to="Order",
                              on_delete=models.SET_NULL,
                              null=True, blank=True,
                              related_name="comments")
    author = models.ForeignKey(to=User,
                               on_delete=models.SET_NULL,
                               null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=1000)

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return self.content
