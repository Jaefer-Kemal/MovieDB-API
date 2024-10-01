from django.contrib import admin
from movie_info.models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "active")
    search_fields = ("name", "description")
    list_filter = ("active",)
