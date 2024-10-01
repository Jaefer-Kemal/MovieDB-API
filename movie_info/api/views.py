from rest_framework.response import Response
from rest_framework import status
from movie_info.models import Movie
from movie_info.api.serializers import MovieSerializer
# from rest_framework.decorators import api_view


'''
This is the pervious version using function-based views. 1st version'''
# @api_view(["GET"])
# def movie_list(request):
#     try:
#         movies = Movie.objects.all()
#     except Movie.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     serializer = MovieSerializer(movies, many=True)

#     return Response(serializer.data, status=status.HTTP_200_OK)


# @api_view(["GET"])
# def movie_details(request, pk):
#     try:
#         movie = Movie.objects.get(pk=pk)
#     except Movie.DoesNotExist:
#         return Response({"Error": "Movie does not exist"}, status=status.HTTP_404_NOT_FOUND)
#     serializer = MovieSerializer(movie)
#     return Response(serializer.data, status=status.HTTP_200_OK)

# @api_view(["POST"])
# def movie_create(request):
#     try:
#         serializer = MovieSerializer(data=request.data)
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
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
    
#     if request.method == "DELETE":
#         movie.delete()
#         return Response({"message": "Movie deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
#     if request.method == "PUT":
    
#         serializer = MovieSerializer(movie, data=request.data)
       
        
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
from rest_framework.views import APIView
from rest_framework import pagination
'''This is the new version using class-based views specifically APIView. 2nd version'''

class MovieListAV(APIView):
    def get(self, request):
        try:
            movies = Movie.objects.all()
            # Instantiate a pagination object
            paginator = pagination.PageNumberPagination()
            # Get the 'page_size' from query parameters, defaulting to 10 if not provided
            paginator.page_size = request.GET.get('page_size', 10)
            # Apply pagination to the queryset
            movies_paginated = paginator.paginate_queryset(movies, request)
        
            # Serialize the paginated data
            serializer = MovieSerializer(movies_paginated, many=True)
            return Response(serializer.data)
        except Movie.DoesNotExist:
            Response({"Error": "Movie does not exist"}, status=status.HTTP_404_NOT_FOUND)
            
    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MovieDetailAV(APIView):
    def get(self, request, pk):
        try:
            movie = Movie.objects.get(pk=pk)
            serializer = MovieSerializer(movie)
            return Response(serializer.data)
        except Movie.DoesNotExist:
            return Response({"Error": "Movie does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, pk):
        try:
            movie = Movie.objects.get(pk=pk)
            serializer = MovieSerializer(movie, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Movie.DoesNotExist:
            return Response({"Error": "Movie does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, pk):
        try:
            movie = Movie.objects.get(pk=pk)
            movie.delete()
            return Response({"message": "Movie deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Movie.DoesNotExist:
            return Response({"Error": "Movie does not exist"}, status=status.HTTP_404_NOT_FOUND)