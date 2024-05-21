from rest_framework import serializers
from . models import *

class LearnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Learner
        fields = '__all__'

class EducatorSerializer(serializers.ModelSerializer):
    class Meta :
        model = Educator
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'