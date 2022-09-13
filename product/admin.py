from django.contrib import admin
from .models import *

admin.site.register(Product)
admin.site.register(Likes)
admin.site.register(Comments)
admin.site.register(Favorites)
