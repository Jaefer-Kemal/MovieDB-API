# movies/views.py or movies/csrf_token_view.py
from django.http import JsonResponse
from django.middleware.csrf import get_token

def get_csrf_token(request):
    """
    Returns a JSON response with the CSRF token.
    """
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})
