from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, Http404
from movie_info.models import Movie
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie
import json


def movie_list(request):
    movies = Movie.objects.all()
    data = {"movies": list(movies.values())}
    return JsonResponse(data)


def movie_details(request, pk):
    try:
        movie = get_object_or_404(Movie, pk=pk)
    except Http404:
        return JsonResponse({"detail": "No movie found with this ID"}, status=404)

    data = movie.serializer()

    return JsonResponse(data)


@csrf_exempt
def movie_create(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON data from request body
        except json.JSONDecodeError:
            return JsonResponse({"detail": "Invalid JSON"}, status=400)

        try:
            # Create the Movie instance
            movie = Movie.objects.create(**data)
        except TypeError:
            return JsonResponse({"detail": "Invalid fields provided"}, status=400)

        return JsonResponse(
            movie.serializer(), status=201
        )  # Assuming the Movie model has a serialize method

    return JsonResponse({"detail": "Invalid request method"}, status=400)

@csrf_exempt
def movie_update(request, pk):
    if request.method == "PUT":
        # Retrieve the movie instance using the primary key (pk)
        movie = get_object_or_404(Movie, pk=pk)

        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"detail": "Invalid JSON format"}, status=400)

        print(data)
        # Update the movie fields with the provided data
        movie.name = data.get("name", movie.name)
        movie.description = data.get("description", movie.description)
        movie.active = data.get("active", movie.active)

        try:
            # Save the updated movie instance
            movie.save()
        except Exception as e:
            return JsonResponse({"detail": f"Update failed: {str(e)}"}, status=400)
        movies = Movie.objects.all()
        # Return the updated serialized movie object as a response
        data = [ movie.serializer() for movie in movies]
        return JsonResponse({"movies":data }, status=200)

    # Return an error response if the request method is not PUT
    return JsonResponse({"detail": "Invalid request method"}, status=400)

@csrf_protect
@ensure_csrf_cookie
def movie_delete(request, pk):
    if request.method == "DELETE":
        try:
            movie = get_object_or_404(Movie, pk=pk)
            deleted = movie.delete()
        except Exception as e:
            return JsonResponse({"detail": f"Delete failed: {str(e)}"}, status=400)
        return JsonResponse({"detail": f"Movie with ID {pk} deleted successfully"}, status=200)
    return JsonResponse({"detail": "Invalid request method"}, status=400)