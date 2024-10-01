from django.urls import path
# from movie_info.api.views import movie_list, movie_details, movie_create, movie_update_delete

'''This is the first url used in function-based views. 1st version'''
# urlpatterns = [
#     path("list/", movie_list, name="movie_list"),
#     path("<int:pk>", movie_details, name="movie_details"),
#     path("create", movie_create, name="movie_create"),
#     path('<int:pk>/up_del/', movie_update_delete, name='movie-update-delete'),
# ]

'''This is the second url used in class-based views specifically APIView. 2nd version'''
from movie_info.api.views import MovieListAV, MovieDetailAV
urlpatterns = [
    path("list/",MovieListAV.as_view(), name="movie_list"),
    path("<int:pk>", MovieDetailAV.as_view(), name="movie_details"),
    
]