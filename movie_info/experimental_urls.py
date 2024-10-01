from movie_info.experimental_views import movie_list, movie_details, movie_create, movie_update, movie_delete
from .csrf_token_view import get_csrf_token
from django.urls import path

urlpatterns = [
    path("list/", movie_list, name="movie_list"),  # API endpoint for listing all movies
    path(
        "<int:pk>", movie_details, name="movie_details"
    ),  # API endpoint for individual movies
    path(
        "create/", movie_create, name="movie_create"
        
    ),  # API endpoint for creating new movies
    path("update/<int:pk>/", movie_update, name="movie_update"),
    path("delete/<int:pk>/", movie_delete, name="movie_delete"),
    path('get-csrf-token/', get_csrf_token, name='get-csrf-token')
]
