from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


class Student(models.Model):
    username = models.CharField(max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(blank=True, null=True)
    major = models.CharField(max_length=50)
    gpa = models.DecimalField(max_digits=3, decimal_places=2)
    auth0_id = models.CharField(max_length=255, blank=True, null=True)


class Teacher(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField(blank=True, null=True)
    teacher_id = models.CharField(max_length=10, unique=True)
    years_of_experience = models.PositiveIntegerField()
    specialization = models.CharField(max_length=100)
    auth0_id = models.CharField(max_length=255, blank=True, null=True)


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Teacher, on_delete=models.CASCADE)


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2, null=True)


class Assignment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    due_date = models.DateField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
