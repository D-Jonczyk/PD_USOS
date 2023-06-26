from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save


class Auth0User(AbstractUser):
    nickname = models.CharField(max_length=255, unique=True)
    password = None
    last_login = None
    first_name = None
    last_name = None
    username = None

    picture = models.URLField()
    given_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    auth0_id = models.CharField(max_length=255, unique=True)

    USERNAME_FIELD = 'auth0_id'

    def __str__(self):
        return self.auth0_id


User = get_user_model()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        if instance.teacher:
            instance.teacher.save()
    except ObjectDoesNotExist:
        pass

    try:
        if instance.student:
            instance.student.save()
    except ObjectDoesNotExist:
        pass


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    subject = models.CharField(max_length=100)

    def __str__(self):
        return self.user.name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # add any additional fields that you want
    grade = models.IntegerField(default=0)

    def __str__(self):
        return self.user.name


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    instructor = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)  # Link course to a teacher


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    # Add an instructor field here
    grade = models.CharField(max_length=2, null=True, blank=True)  # Keeping this optional

    class Meta:
        unique_together = ('student', 'course')


class Assignment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    due_date = models.DateField()
