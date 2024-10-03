from django.urls import path

# from movie_info.api.views import movie_list, movie_details, movie_create, movie_update_delete

"""This is the first url used in function-based views. 1st version"""
# urlpatterns = [
#     path("list/", movie_list, name="movie_list"),
#     path("<int:pk>", movie_details, name="movie_details"),
#     path("create", movie_create, name="movie_create"),
#     path('<int:pk>/up_del/', movie_update_delete, name='movie-update-delete'),
# ]

"""This is the second url used in class-based views specifically APIView. 2nd version"""
from movie_info.api.views import (
    MovieListAV,
    MovieDetailAV,
    # StreamingPlatformListAV,
    # StreamingPlatformDetailAV,
    ReviewDetail,
    ReviewList,
    ReviewCreate
)

urlpatterns = [
    path("list/", MovieListAV.as_view(), name="movie_list"),
    path("<int:pk>/", MovieDetailAV.as_view(), name="movie_details"),
    # path("stream/", StreamingPlatformListAV.as_view(), name="stream_list"),
    # path("stream/<int:pk>", StreamingPlatformDetailAV.as_view(), name = "stream_details"),
    path("<int:pk>/reviews/", ReviewList.as_view(), name="review_list"),
    path("review/<int:pk>/", ReviewDetail.as_view(), name="review_details"),
    path("<int:pk>/review-create/", ReviewCreate.as_view(), name="review_create")
]

from rest_framework.routers import DefaultRouter
from movie_info.api.views import StreamingPlatformVS
router = DefaultRouter()
router.register(r'stream', StreamingPlatformVS, basename='stream')  
# Since the basename is stream, if we want to use reverse() in our views,
# we need to use 'stream-list' instead of 'stream' to access the list view.
# and if we want to access the detail view, we need to use 'stream-detail'

urlpatterns += router.urls