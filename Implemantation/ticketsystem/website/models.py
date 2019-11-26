from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models


class Ticket(models.Model):
    price = models.IntegerField()
    seat_number = models.CharField(max_length=10)


class User(AbstractUser):
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
    state = models.CharField(max_length=10)
    img = models.URLField(null=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Admin(User):
    pass


class Operator(User):
    pass


class Visitor(models.Model):
    pass


class Stage(models.Model):
    place = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    quota = models.IntegerField()


class Event(models.Model):
    name = models.CharField(max_length=50)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    date = models.DateField()
    quota = models.IntegerField()
    isAvailable = models.BooleanField(default=False)
    isAccepted = models.BooleanField(default=False)
    rules = models.CharField(max_length=500)


class Concert(Event):
    pass


class Theatre(Event):
    pass


class Sport(Event):
    pass
