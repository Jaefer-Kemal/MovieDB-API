from rest_framework.response import Response
from rest_framework import status
from movie_info.models import MovieList, StreamingPlatform, Review

from movie_info.api.serializers import MovieListSerializer, StreamingPlatformSerializer

# from rest_framework.decorators import api_view
from rest_framework import generics, mixins

from .serializers import ReviewSerializer
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import status

from rest_framework.exceptions import ValidationError

from movie_info.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from rest_framework import permissions
"""1. 
This is the pervious version using function-based views. 1st version"""
# @api_view(["GET"])
# def movie_list(request):
#     try:
#         movies = Movie.objects.all()
#     except Movie.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     serializer = MovieListSerializer(movies, many=True)

#     return Response(serializer.data, status=status.HTTP_200_OK)


# @api_view(["GET"])
# def movie_details(request, pk):
#     try:
#         movie = Movie.objects.get(pk=pk)
#     except Movie.DoesNotExist:
#         return Response({"Error": "Movie does not exist"}, status=status.HTTP_404_NOT_FOUND)
#     serializer = MovieListSerializer(movie)
#     return Response(serializer.data, status=status.HTTP_200_OK)

# @api_view(["POST"])
# def movie_create(request):
#     try:
#         serializer = MovieListSerializer(data=request.data)
#     except serializer.errors:
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(["PUT", "DELETE","GET"])
# def movie_update_delete(request, pk):

#     try:
#         movie = Movie.objects.get(pk=pk)
#     except Movie.DoesNotExist:
#         return Response({"Error" : "Movie does not exist"},status=status.HTTP_404_NOT_FOUND)


#     if request.method == "GET":
#         serializer = MovieListSerializer(movie)
#         return Response(serializer.data, status=status.HTTP_200_OK)


#     if request.method == "DELETE":
#         movie.delete()
#         return Response({"message": "Movie deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

#     if request.method == "PUT":

#         serializer = MovieListSerializer(movie, data=request.data)


#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""2. This is the new version using class-based views specifically APIView. 2nd version"""

from rest_framework.views import APIView
from rest_framework import pagination


class MovieListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request):
        try:
            movies = MovieList.objects.all()
            # Instantiate a pagination object
            paginator = pagination.PageNumberPagination()
            # Get the 'page_size' from query parameters, defaulting to 10 if not provided
            paginator.page_size = request.GET.get("page_size", 10)
            # Apply pagination to the queryset
            movies_paginated = paginator.paginate_queryset(movies, request)

            # Serialize the paginated data
            serializer = MovieListSerializer(movies_paginated, many=True)
            return Response(serializer.data)
        except MovieList.DoesNotExist:
            Response(
                {"Error": "Movie does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request):
        serializer = MovieListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request, pk):
        try:
            movie = MovieList.objects.get(pk=pk)
            serializer = MovieListSerializer(movie)
            return Response(serializer.data)
        except MovieList.DoesNotExist:
            return Response(
                {"Error": "Movie does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, pk):
        try:
            movie = MovieList.objects.get(pk=pk)
            serializer = MovieListSerializer(movie, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except MovieList.DoesNotExist:
            return Response(
                {"Error": "Movie does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, pk):
        try:
            movie = MovieList.objects.get(pk=pk)
            movie.delete()
            return Response(
                {"message": "Movie deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )
        except MovieList.DoesNotExist:
            return Response(
                {"Error": "Movie does not exist"}, status=status.HTTP_404_NOT_FOUND
            )


# 3. This is using APIVIEW BUT WE WILL CONVERT IT INTO MODELVIEWSET in the later secion
"""
class StreamingPlatformListAV(APIView):
    def get(self, request):
        try:
            platforms = StreamingPlatform.objects.all()
            serializer = StreamingPlatformSerializer(platforms, many=True)
            return Response(serializer.data)

        except StreamingPlatform.DoesNotExist:
            return Response({"Error": "Streaming platform does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
    def post(self, request):
        serializer = StreamingPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class StreamingPlatformDetailAV(APIView):
    def get(self, request, pk):
        try:
            platform = StreamingPlatform.objects.get(pk=pk)
            serializer = StreamingPlatformSerializer(platform)
            return Response(serializer.data)
        except StreamingPlatform.DoesNotExist:
            return Response({"Error": "Streaming platform does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, pk):
        try:
            platform = StreamingPlatform.objects.get(pk=pk)
            serializer = StreamingPlatformSerializer(platform, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except StreamingPlatform.DoesNotExist:
            return Response({"Error": "Streaming platform does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, pk):
        try:
            platform = StreamingPlatform.objects.get(pk=pk)
            platform.delete()
            return Response({"message": "Streaming platform deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except StreamingPlatform.DoesNotExist:
            return Response({"Error": "Streaming platform does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
"""

"""4. WE are using ModelViewset for this"""
from rest_framework import viewsets


class StreamingPlatformVS(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = StreamingPlatform.objects.all()
    serializer_class = StreamingPlatformSerializer


"""5. Concrete version using GenericAPIView and mixins"""


# List and Create Reviews
class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return Review.objects.filter(movielist=pk)


# Retrieve, Update, and Delete Reviews
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Review.objects.all()
    def perform_create(self, serializer):
        pk = self.kwargs.get("pk")
        movie = MovieList.objects.get(pk=pk)
        review_user = self.request.user
        review_queryset = Review.objects.filter(movielist=movie, review_user=review_user)
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie.")
        serializer.save(movielist=movie, review_user=review_user)

    def get(self, request, *args, **kwargs):
        """Override GET method to display a custom message for unsupported GET requests."""
        return Response(
            {"detail": "You can only submit a POST request to create a new review."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )


class APIRootView(APIView):
    """
    API Overview for MovieDB.
    Provides a structured overview of all available endpoints, descriptions, and usage examples.
    """

    def get(self, request, *args, **kwargs):
        api_overview = {
            "Welcome to MovieDB API": "A comprehensive API for managing movies, streaming platforms, and reviews.",
            "To Access the AdminPanel": reverse("admin:index", request=request),
            "Movies": {
                "List Movies": {
                    "url": reverse("movie_list", request=request),
                    "description": "Get a list of all available movies in the database.",
                    "methods": ["GET"],
                }
            },
            "Movie Details": {
                "url": reverse("movie_details", kwargs={"pk": 1}, request=request),
                "description": "Retrieve details of a specific movie using its ID.",
                "methods": ["GET"],
            },
            "Streaming Platforms": {
                "List Platforms": {
                    "url": reverse("stream-list", request=request),
                    "description": "Get a list of all streaming platforms.",
                    "methods": ["GET"],
                },
                "Platform Details": {
                    "url": reverse("stream-detail", kwargs={"pk": 2}, request=request),
                    "description": "Retrieve details of a specific platform using its ID.",
                    "methods": ["GET"],
                },
            },
            "Reviews": {
                "List Reviews for a Movie": {
                    "url": reverse("review_list", kwargs={"pk": 1}, request=request),
                    "description": "List all reviews for a specific movie using its movie ID.",
                    "methods": ["GET"],
                },
                "Create a Review": {
                    "url": reverse("review_create", kwargs={"pk": 1}, request=request),
                    "description": "Create a new review for a specific movie using its movie ID.",
                    "methods": ["POST"],
                },
                "Review Details": {
                    "url": reverse("review_details", kwargs={"pk": 1}, request=request),
                    "description": "Retrieve, update, or delete a specific review using its ID.",
                    "methods": ["GET", "PUT", "DELETE"],
                },
            },
        }
        return Response(api_overview, status=status.HTTP_200_OK)


# 6. USING GenericAPIView with Mixins
#  List and Create combined using Mixins and GenericAPIView
"""
class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)  # List all reviews

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)  # Create a new review
"""
# Retrieve, Update, and Delete combined
"""
class ReviewDetail(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin, 
                   mixins.DestroyModelMixin,
                   generics.GenericAPIView):
    
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)  # Retrieve a single review

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)  # Update a review

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)  # Delete a review
    
"""