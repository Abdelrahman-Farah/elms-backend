from rest_framework import serializers
from .models import Course, CourseLearner, Learner, Post


# Define serializer for enrolling in a course
class CourseEnrollSerializer(serializers.ModelSerializer):
    # Specify the model and fields to be serialized
    join_code = serializers.CharField(max_length=7)

    class Meta:
        model = Course
        fields = ["join_code"]


# Define serializer for Course model
class CourseSerializer(serializers.ModelSerializer):
    # Specify the model and fields to be serialized
    join_code = serializers.CharField(max_length=7, read_only=True)
    owner = serializers.SerializerMethodField(read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = ["id", "owner", "title", "avatar", "join_code", "description"]

    # Define custom method to get owner details
    def get_owner(self, obj):
        return {
            "id": obj.owner.id,
            "username": obj.owner.username,
            "email": obj.owner.email,
        }


# Define serializer for Post mode
class PostSerializer(serializers.ModelSerializer):

    # Specify the model and fields to be serialized
    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "description",
            "image",
            "file",
            "video",
            "created_at",
            "updated",
        ]

    # Override the create method to handle owner separately
    def create(self, validated_data):
        owner = validated_data.pop("owner")
        post = Post.objects.create(**validated_data)
        post.owner = owner
        post.save()
        return post

# Define serializer for Learner mode
class CourseLearnerSerializer(serializers.ModelSerializer):
    learner = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CourseLearner
        fields = ["learner"]


    # Define custom method to get learner details
    def get_learner(self, obj):
        return {
            "id": obj.learner.id,
            "username": obj.learner.user.username,
            "email": obj.learner.user.email,
        }

    