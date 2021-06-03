from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import Token
from courses.models import Course
#
# class CoursesTests(APITestCase):
#
#     def setUp(self):
#
#         user_test1 = User.objects.create_user(username='test1', password='cvbnm,./', level='teacher')
#         user_test1.save()
#         user_test2 = User.objects.create_user(username='test2', password='cvbnm,./', level='student')
#         user_test2.save()
#
#         self.user_test1_token = Token.objects.create(user=user_test1)
#         self.user_test2_token = Token.objects.create(user=user_test2)


#