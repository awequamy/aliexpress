from termios import OFDEL
from django.contrib import admin

from account.models import Contact
from .models import Order
# Register your models here.
admin.site.register(Order)

