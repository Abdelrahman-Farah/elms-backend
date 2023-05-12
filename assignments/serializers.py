from rest_framework import serializers
from .models import CourseAssignment, AssignmentSubmission


class CourseAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseAssignment
        fields = ['id', 'title', 'description', 'due_date',
                  'degree', 'file', 'Image', 'video', 'created_at']


class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    score = serializers.IntegerField(read_only=True)

    class Meta:
        model = AssignmentSubmission
        fields = ['id',
                  'status',
                  'notes',
                  'score',
                  'Image',
                  'file',
                  'video',
                  ]


class AssignmentSubmissionForOwnerSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = AssignmentSubmission
        fields = ['id',
                  'student',
                  'status',
                  'score',
                  'notes',
                  'file',
                  'video',
                  'Image',
                  'time',
                  ]

    def get_student(self, obj):
        return {
            "id": obj.student.id,
            "username": obj.student.username,
            "email": obj.student.email,
        }
