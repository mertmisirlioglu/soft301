from django.db import models
from django.contrib.auth.models import User


class Stage(models.Model):
    place = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    quota = models.IntegerField()

    def __str__(self):
        return '' + self.place


class Event(models.Model):
    TYPE = (
        ('C', 'Concert'),
        ('T', 'Theatre'),
        ('S', 'Sports')
    )
    name = models.CharField(max_length=50)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateField()
    quota = models.IntegerField()
    price = models.IntegerField()
    type = models.CharField(max_length=1, choices=TYPE)
    isAvailable = models.BooleanField(default=False)
    isAccepted = models.BooleanField(default=False)
    rules = models.CharField(max_length=500)
    img = models.URLField(null=True, blank=True)

    def get_preview_ticket_url(self):
        return f"/event/{self.pk}/preview"

    def get_buy_ticket_url(self):
        return f"/event/{self.pk}/buy"

    def get_approve_url(self):
        return f"/admin/event/approve/{self.pk}"

    def __str__(self):
        return '' + self.name


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def get_ticket_review_url(self):
        return f"/account/tickets/{self.pk}/preview"


class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    gender = models.CharField(max_length=1, choices=GENDER)

    birthday = models.DateField()
    phone_number = models.CharField(max_length=11)
    img = models.URLField(null=True, blank=True)
    isOperator = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


