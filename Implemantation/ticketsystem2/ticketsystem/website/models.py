from django.db import models
from django.contrib.auth.models import User


class Stage(models.Model):
    place = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    quota = models.IntegerField()

    def __str__(self):
        return '' + self.place


class Event(models.Model):
    name = models.CharField(max_length=50)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    date = models.DateField()
    quota = models.IntegerField()
    price = models.IntegerField()
    isAvailable = models.BooleanField(default=False)
    isAccepted = models.BooleanField(default=False)
    rules = models.CharField(max_length=500)

    def get_preview_ticket_url(self):
        return f"/event/{self.pk}/preview"

    def get_buy_ticket_url(self):
        return f"/event/{self.pk}/buy"

    def __str__(self):
        return '' + self.name


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER)
    email = models.EmailField(primary_key=True)
    birthday = models.DateField()
    phone_number = models.CharField(max_length=11)
    password = models.CharField(max_length=20)
    state = models.CharField(max_length=10, null=True, blank=True)
    img = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class Operator(UserProfile):
    pass


class Visitor(models.Model):
    pass


class Concert(Event):
    pass


class Theatre(Event):
    pass


class Sport(Event):
    pass
