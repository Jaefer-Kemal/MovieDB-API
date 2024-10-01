from rest_framework import serializers
from movie_info.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    active = serializers.BooleanField()

    class Meta:
        model = Movie
        fields = ("id", "name", "description", "active")
        
    def create(self,validated_data):
        return Movie.objects.create(**validated_data)
    
    def update(seld,instance,validated_data):
        instance.name = validated_data.get("name",instance.name)
        instance.description = validated_data.get("description",instance.description)
        instance.active = validated_data.get("active",instance.active)
        instance.save()
        
        return instance
