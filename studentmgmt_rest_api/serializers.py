from rest_framework import serializers
from .models import Student, Course, Department, Teacher, Enrollment, Assignment, \
    Auth0User


class Auth0UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auth0User
        fields = ['nickname', 'is_superuser', 'email', 'picture', 'given_name', 'name', 'auth0_id']


class StudentSerializer(serializers.ModelSerializer):
    user = Auth0UserSerializer()  # Nested serializer to show user details

    class Meta:
        model = Student
        fields = '__all__'


class EnrollmentSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name')
    grade = serializers.CharField()
    student = StudentSerializer()

    class Meta:
        model = Enrollment
        fields = ['course_id', 'course_name', 'student', 'grade']


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'description']


class TeacherSerializer(serializers.ModelSerializer):
    user = Auth0UserSerializer()  # Nested serializer to show user details

    class Meta:
        model = Teacher
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    instructor = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all())

    class Meta:
        model = Course
        fields = '__all__'


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'name', 'description', 'course', 'due_date', 'student']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        enrollment = Enrollment.objects.filter(student=instance.student, course=instance.course).first()
        representation['grade'] = enrollment.grade if enrollment else None
        return representation
