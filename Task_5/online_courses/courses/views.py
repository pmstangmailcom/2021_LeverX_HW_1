from django.shortcuts import render
from rest_framework import status, generics, permissions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import *
from .serializers import *


class UserCreate(APIView):
    """Creates the user."""
    permission_classes = (AllowAny,)

    def post(self, request, format='json'):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseListView(generics.ListAPIView):
    """Displaying the courses list"""
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer


class CourseDetailView(generics.RetrieveAPIView):
    """Displaying the full course description"""
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = [IsOwner]


class CourseCreateView(generics.CreateAPIView):
    """Create course"""
    serializer_class = CourseCreateSerializer
    permission_classes = [IsTeacher]

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


class CourseUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """Update or delete course"""
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = [IsTeacher, IsOwner]
