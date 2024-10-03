from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class StreamingPlatform(models.Model):
    name = models.CharField(max_length=40)
    about = models.TextField(max_length=200)
    website = models.URLField(max_length=200)
    
    def __str__(self):
        return self.name


class MovieList(models.Model):
    title = models.CharField(max_length=100)
    storyline = models.TextField(max_length=200)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    platform = models.ForeignKey(StreamingPlatform, on_delete=models.CASCADE, related_name="movielist")
    
    
    def __str__(self):
        return self.title
    
    def serializer(self):
        return {
            "id":self.id,
            "name": self.title,
            "description": self.description,
            "active": self.active,
        }


class Review(models.Model):
    review_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews",default=1)  # User who wrote the review
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])  # Rating from 1 to 5
    description = models.CharField(max_length=300, null=True)  # Optional review description
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-set at creation
    updated_at = models.DateTimeField(auto_now=True)  # Auto-set at every update
    
    # ForeignKey relationship to MovieList
    movielist = models.ForeignKey(
        MovieList, 
        on_delete=models.CASCADE, 
        related_name="reviews"  # Related name for reverse lookup
    )
    
    def __str__(self):
        return f"{self.rating} | {self.movielist.title}"  