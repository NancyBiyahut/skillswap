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
    tag_names = serializers.SerializerMethodField()
    class Meta:
        model = Session
        fields = '__all__'
    def get_tag_names(self, obj):
        return [tag.name for tag in obj.tags.all()]
    
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'