from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import LEVEL, User, Course


class UserCreateSerializer(serializers.ModelSerializer):
    """Displaying User registration"""
    level = serializers.ChoiceField(choices=LEVEL)
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(max_length=32, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'level')


class CourseListSerializer(serializers.ModelSerializer):
    """Displaying the courses list"""

    class Meta:
        model = Course
        fields = ('id', 'name')


class CourseCreateSerializer(serializers.ModelSerializer):
    """Displaying the course creation"""
    lecture_to_course = serializers.StringRelatedField(many=True)
    course_teacher = serializers.StringRelatedField(many=True)
    course_student = serializers.StringRelatedField(many=True)
    teacher = serializers.ReadOnlyField(source='user.username')
    # owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(serializers.ModelSerializer):
    """Displaying the full course description"""
    lectures_to_course = serializers.StringRelatedField(many=True)
    teacher = serializers.StringRelatedField(many=True)
    student = serializers.StringRelatedField(many=True)

    class Meta:
        model = Course
        fields = ('id', 'name', 'lectures_to_course', 'teacher', 'student')


class LectureCreateSerializer(serializers.ModelSerializer):
    """Displaying the lecture creation"""

    class Meta:
        model = Course
        fields = ('subject', 'file')