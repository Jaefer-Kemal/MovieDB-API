from rest_framework import serializers
from movie_info.models import Movie


def length_check(value):
    if len(value) < 2:
        raise serializers.ValidationError(f"The title: '{value}' is too short")


class MovieSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(validators=[length_check])
    description = serializers.CharField()
    active = serializers.BooleanField()

    class Meta:
        model = Movie
        fields = ("id", "name", "description", "active")

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.active = validated_data.get("active", instance.active)
        instance.save()

        return instance

    def validate_description(self, value):
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
                "The description should not exceed 200 characters"
            )
        if any(word in value.lower() for word in forbidden_words):
            raise serializers.ValidationError(
                "The description should not contain explicit offensive language"
            )
        return value
    
    def validate(self, data):
        if data["name"] == data["description"]:
            raise serializers.ValidationError(
                "The name and description should not be the same"
            )
