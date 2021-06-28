from django.contrib import admin
from .models import Movie, Review, Rank, Comment

# Register your models here.
admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Rank)
admin.site.register(Comment)