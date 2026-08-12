from django.db import models


# Create your models here.

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

    def __str__(self):
        return f"{self.make} {self.model}"


class Order(models.Model):
    car = models.ForeignKey(to="Car",
                            on_delete=models.SET_NULL,
                            null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    LOAN_STATUS = (
        ('p', 'Patvirtinta'),
        ('v', 'Vykdoma'),
        ('i', 'Įvykdyta'),
        ('a', 'Atmesta'),
    )

    status = models.CharField(choices=LOAN_STATUS, default='p')

    def total(self):
        result = 0
        for line in self.lines.all():
            result += line.service.price * line.quantity
        return result

    def __str__(self):
        return f"{self.car} ({self.date})"


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
