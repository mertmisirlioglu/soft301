from django.contrib.auth.models import User
from django.db import models


class Ticket(models.Model):
    price = models.IntegerField()
    seat_number = models.CharField(max_length=10)


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER)
    birthday = models.DateField()
    phone_number = models.CharField(max_length=11)
    password = models.CharField(max_length=20)
    state = models.CharField(max_length=10,null=True,blank=True)
    img = models.URLField(null=True,blank=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, null=True,blank=True)

    def __str__(self):
    	return self.user.username



class Operator(UserProfile):
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
