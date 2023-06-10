from rest_framework import serializers
from .models import Course, CourseLearner, Learner, Post, PostFiles


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
    isOwner = serializers.SerializerMethodField(read_only=True, source="owner")

    class Meta:
        model = Course
        fields = ["id", "owner", "title", "avatar", "join_code", "description", "isOwner", "created_at"]

    # Define custom method to get owner details
    def get_owner(self, obj):
        return {
            "id": obj.owner.id,
            "username": obj.owner.username,
            "email": obj.owner.email,
        }
    
    def get_isOwner(self, obj):
        request = self.context.get('request')
        if request:
            if obj.owner == request.user:
                return True
        return False

class PostFilesSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        post_id = self.context.get("post_id")
        return PostFiles.objects.create(post_id=post_id, **validated_data)
    class Meta:
        model = PostFiles
        fields = ["id", "file", "file_type", "title"]


# Define serializer for Post mode
class PostSerializer(serializers.ModelSerializer):
    files = PostFilesSerializer(many=True, required=False)
    isOwner = serializers.SerializerMethodField(read_only=True, source="owner")
    # Specify the model and fields to be serialized
    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "description",
            "files",
            "created_at",
            "updated",
            "isOwner",
        ]

    # Override the create method to handle owner separately
    def create(self, validated_data):
        owner = validated_data.pop("owner")
        files_data = self.context["files"]
        post = Post.objects.create(**validated_data)
        post.owner = owner
        post.save()
        for file_data in files_data:
            PostFiles.objects.create(post=post, file=file_data, file_type=file_data.content_type, title=file_data.name)
        return post
    
    def get_isOwner(self, obj):
        request = self.context.get('request')
        if request:
            if obj.course.owner_id == request.user.id:
                return True
        return False

# Define serializer for Learner mode
class CourseLearnerSerializer(serializers.ModelSerializer):
    learner = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CourseLearner
        fields = ["id", "learner"]


    # Define custom method to get learner details
    def get_learner(self, obj):
        return {
            "id": obj.learner.id,
            "username": obj.learner.user.username,
            "email": obj.learner.user.email,
        }


