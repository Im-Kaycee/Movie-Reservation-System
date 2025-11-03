from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id','name']
class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = ['id','title', 'description', 'genres', 'poster_image', 'duration', 'created_at']
        
