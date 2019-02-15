from django.contrib import admin
from recommend.models import UserRating, Movie

admin.site.register(Movie)
admin.site.register(UserRating)
