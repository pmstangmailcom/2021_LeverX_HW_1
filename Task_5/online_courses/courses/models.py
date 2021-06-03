from django.contrib.auth.models import AbstractUser
from django.db import models

LEVEL = [
    ('teacher', 'Teacher'),
    ('student', 'Student'),
]


class User(AbstractUser):
    """Extend the User class by a choicefield, whether user is a teacher or a student"""
    username = models.CharField(db_index=True, max_length=50, unique=True, blank=False)
    email = models.EmailField(max_length=100)
    level = models.CharField(max_length=20, verbose_name='level', choices=LEVEL, default='student')


class Course(models.Model):
    """Courses model"""
    name = models.CharField(max_length=150, verbose_name='course')
    teacher = models.ManyToManyField(User, related_name='course_teacher', verbose_name='course_teacher', blank=True)
    student = models.ManyToManyField(User, related_name='course_student', verbose_name='course_student', blank=True)
    # owner = models.ForeignKey(User, related_name='courses', verbose_name='owner', on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.name


class Lecture(models.Model):
    """Lecture for the course"""
    subject = models.CharField(max_length=150, verbose_name='subject', )
    file = models.FileField(upload_to='uploads/')
    course = models.ForeignKey(Course, related_name='lectures_to_course', verbose_name='course',
                               on_delete=models.CASCADE)

    def __str__(self):
        return self.subject


class HomeWork(models.Model):
    """Homework for the lecture"""
    task = models.TextField(verbose_name='task', blank=False)
    solution = models.TextField(verbose_name='solution', blank=True)
    is_done = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    lecture = models.ForeignKey(Lecture, related_name='homework_to_lecture', verbose_name='lecture',
                                on_delete=models.CASCADE)

    def __str__(self):
        return 'Homework for the lecture{}'.format(self.lecture)


class Solution(models.Model):
    """Solution for the homework"""
    solution = models.TextField(verbose_name='solution', blank=True)
    homework = models.ForeignKey(HomeWork, related_name='solutions_homework', verbose_name='homework',
                                 on_delete=models.CASCADE)


class Mark(models.Model):
    """Mark for the homework solution"""
    value = models.PositiveIntegerField(verbose_name='mark', default=0)
    homework = models.ForeignKey(Solution, related_name='marks_to_solution', verbose_name='homework',
                                 on_delete=models.CASCADE)

    def __str__(self):
        return 'Mark {} for the {}'.format(self.value, self.homework)


#
#
class Comment(models.Model):
    """Comment for the mark"""
    text = models.TextField(verbose_name='task', blank=True)
    mark = models.ForeignKey(Mark, related_name='comments_to_mark', verbose_name='mark',
                             on_delete=models.CASCADE)
