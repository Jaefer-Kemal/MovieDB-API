from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from .models import Review, MovieList

@receiver(post_save, sender=Review)
def update_movie_rating_on_save(sender, instance, created, **kwargs):
    """
    Update the average rating and number of ratings when a review is added or updated.
    """
    movie = instance.movielist
    movie.number_rating = movie.reviews.count()
    movie.avg_rating = movie.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    movie.save()

@receiver(post_delete, sender=Review)
def update_movie_rating_on_delete(sender, instance, **kwargs):
    """
    Update the average rating and number of ratings when a review is deleted.
    """
    movie = instance.movielist
    movie.number_rating = movie.reviews.count()
    movie.avg_rating = movie.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    movie.save()
