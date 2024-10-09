from django.contrib import admin
from movie_info.models import MovieList, StreamingPlatform, Review


@admin.register(MovieList)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "storyline",
        "active",
        "created_at",
        "number_rating",
        "avg_rating",
    )
    search_fields = ("title", "storyline")
    list_filter = ("active",)


admin.site.register(StreamingPlatform)
admin.site.register(Review)
