from rest_framework import serializers
from movie_info.models import MovieList, StreamingPlatform, Review
from django.utils import timezone


def length_check(value):
    if len(value) < 2:
        raise serializers.ValidationError(f"The title: '{value}' is too short")


class ReviewSerializer(serializers.ModelSerializer):
    movie = serializers.SerializerMethodField()
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        # fields = "__all__"
        exclude = ["movielist"]
    def get_movie(self, obj):
        return obj.movielist.title
    
class MovieListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(validators=[length_check])

    # Custom field use serializers.SerializerMethodField
    len_title = serializers.SerializerMethodField()
    since_created = serializers.SerializerMethodField()
    stream = serializers.SerializerMethodField()
    
    #Nested Serializer
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = MovieList
        fields = (
            "id",
            "title",
            "len_title",
            "storyline",
            "active",
            "created_at",
            "since_created",
            "platform",
            "stream",
            "reviews",
            "avg_rating",
            "number_rating"
        )

    def get_stream(self, obj):
        # return StreamingPlatform.objects.filter(movielist=obj).first().name
        return obj.platform.name if obj.platform else "No platform"

    def get_len_title(self, object):
        length = len(object.title)
        return length

    def get_since_created(self, obj):
        # Ensure created_at is timezone-aware
        created_at = obj.created_at
        # Calculate the time difference
        time_difference = timezone.now() - created_at
        # Convert time difference to days and hours
        days = time_difference.days
        hours = time_difference.seconds // 3600
        # Return formatted string
        return f"{days} days and {hours} hours" if days > 0 else f"{hours} hours"

    def validate_storyline(self, value):
        forbidden_words = [
            "fuck",
            "shit",
            "damn",
            "bitch",
            "asshole",
            "slut",
            "cunt",
        ]
        if len(value) > 200:
            raise serializers.ValidationError(
                "The storyline should not exceed 200 characters"
            )
        if any(word in value.lower() for word in forbidden_words):
            raise serializers.ValidationError(
                "The storyline should not contain explicit offensive language"
            )
        return value

    def validate(self, data):
        if data["title"] == data["storyline"]:
            raise serializers.ValidationError(
                "The title and storyline should not be the same"
            )
        return data

    """Those methods create and update are only needed for serializer.Serializer and 
    it's not needed for ModelSerializer since its already defined"""
    # def create(self, validated_data):
    #     return Movie.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get("title", instance.title)
    #     instance.storyline = validated_data.get("storyline", instance.storyline)
    #     instance.active = validated_data.get("active", instance.active)
    #     instance.save()

    #     return instance


class StreamingPlatformSerializer(serializers.ModelSerializer):
    movielist = MovieListSerializer(many=True, read_only=True)

    class Meta:
        model = StreamingPlatform
        fields = "__all__"
