from django.db import models

class Movie(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    def serializer(self):
        return {
            "id":self.id,
            "name": self.name,
            "description": self.description,
            "active": self.active,
        }

import random
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create 100 random movie objects"

    def handle(self, *args, **kwargs):
        # Define sample data for movie names and descriptions
        movie_titles = [
            "The Shawshank Redemption", "The Godfather", "The Dark Knight",
            "Pulp Fiction", "Forrest Gump", "Inception", "Fight Club",
            "The Matrix", "Goodfellas", "Interstellar", "Gladiator",
            "Whiplash", "The Social Network", "Parasite", "Mad Max: Fury Road"
        ]
        descriptions = [
            "A story of hope and resilience.", "A gripping crime drama.",
            "A tale of revenge and justice.", "A twisted crime thriller.",
            "An emotional journey of self-discovery.", "A sci-fi thriller.",
            "A battle of wits and will.", "A mind-bending adventure.",
            "A high-octane gangster drama.", "Exploring the cosmos.",
            "A fight for freedom and honor.", "A story of passion and ambition.",
            "The rise of a social empire.", "A dark satire on social classes.",
            "A post-apocalyptic survival saga."
        ]

        # Create 100 random movies
        for _ in range(100):
            Movie.objects.create(
                name=random.choice(movie_titles),
                description=random.choice(descriptions),
                active=random.choice([True, False])
            )

        self.stdout.write(self.style.SUCCESS("Successfully created 100 random movie objects!"))
