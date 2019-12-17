from django.contrib import admin

# Register your models here.
from .models import Event, Stage, Ticket, Concert, Theatre, Sport, UserProfile

admin.site.register(Event)
admin.site.register(Stage)
admin.site.register(UserProfile)
admin.site.register(Ticket)
admin.site.register(Concert)
admin.site.register(Theatre)
admin.site.register(Sport)
