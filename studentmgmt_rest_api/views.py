from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, OR
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Student, Department, Teacher, Course, Enrollment, Assignment
from .serializers import CourseSerializer, DepartmentSerializer, \
    EnrollmentSerializer, AssignmentSerializer, Auth0UserSerializer, TeacherSerializer, StudentSerializer
import jwt
from functools import wraps
from django.http import JsonResponse
from .utils import jwt_decode_token


def get_token_auth_header(request):
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.META.get("HTTP_AUTHORIZATION", None)
    parts = auth.split()
    token = parts[1]

    return token


def requires_scope(required_scope):
    """Determines if the required scope is present in the Access Token
    Args:
        required_scope (str): The scope required to access the resource
    """
    def require_scope(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = get_token_auth_header(args[0])
            decoded = jwt.decode(token, verify=False)
            if decoded.get("scope"):
                token_scopes = decoded["scope"].split()
                for token_scope in token_scopes:
                    if token_scope == required_scope:
                        return f(*args, **kwargs)
            response = JsonResponse({'message': 'You don\'t have access to this resource'})
            response.status_code = 403
            return response
        return decorated
    return require_scope


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'teacher')


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'student')


def get_user_role(user):
    if hasattr(user, 'student'):
        return 'student'
    elif hasattr(user, 'teacher'):
        return 'teacher'
    else:
        return None


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_student_courses(request):
    try:
        student = Student.objects.get(user_id=request.user.id)
        enrollments = student.enrollment_set.all()
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)
    except Student.DoesNotExist:
        return Response({"detail": "Student not found."}, status=404)


@api_view(['POST'])
@permission_classes([IsStudent])
def enroll_in_course(request):
    course_id = request.data.get('course_id')

    try:
        # Use request.user.auth0_id to get the id from the token
        student = Student.objects.get(user_id=request.user.id)
    except Student.DoesNotExist:
        return Response({"detail": "Student not found."}, status=404)

    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return Response({"detail": "Course not found."}, status=404)

    Enrollment.objects.create(student=student, course=course)
    return Response({"detail": "Enrollment successful."}, status=201)


@api_view(['GET'])
@permission_classes([IsTeacher])
def get_teacher_courses(request):
    auth0_id = request.user.id
    try:
        teacher = Teacher.objects.get(user_id=auth0_id)
        courses = teacher.course_set.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)
    except Teacher.DoesNotExist:
        return Response({"detail": "Teacher not found."}, status=404)


# Endpoint for teachers to update the grade of a student in a particular course
@api_view(['PUT'])
@permission_classes([IsTeacher])
def update_student_grade(request, course_id, student_id):
    try:
        teacher = Teacher.objects.get(user_id=request.user.id)
        course = Course.objects.get(id=course_id, instructor=teacher)
    except (Teacher.DoesNotExist, Course.DoesNotExist):
        return Response({"detail": "Teacher or Course not found."}, status=404)

    try:
        enrollment = Enrollment.objects.get(course=course, student_id=student_id)
    except Enrollment.DoesNotExist:
        return Response({"detail": "Enrollment not found."}, status=404)

    grade = request.data.get('grade')
    if grade is not None:
        enrollment.grade = grade
        enrollment.save()
        return Response({"detail": "Grade updated successfully."}, status=200)
    else:
        return Response({"detail": "No grade provided."}, status=400)


@api_view(['GET'])
@permission_classes([IsTeacher])
def get_students_in_course(request, course_id):
    try:
        teacher = Teacher.objects.get(user_id=request.user.id)
        course = Course.objects.get(id=course_id, instructor=teacher)
    except (Teacher.DoesNotExist, Course.DoesNotExist):
        return Response({"detail": "Teacher or Course not found."}, status=404)

    enrollments = Enrollment.objects.filter(course=course)

    # Replace 'EnrollmentSerializer' with the actual name of your enrollment serializer
    serializer = EnrollmentSerializer(enrollments, many=True)
    return Response(serializer.data)


class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = Auth0UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = Auth0UserSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Auth0Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(' ')[1]  # Assuming Bearer token

            try:
                payload = jwt_decode_token(token)
            except jwt.InvalidTokenError:
                request.user = AnonymousUser()
                raise AuthenticationFailed('Invalid token')

            User = get_user_model()
            user_id = payload['sub']
            user, created = User.objects.get_or_create(auth0_id=user_id)
            if created:
                user.nickname = payload.get('nickname', '')
                user.picture = payload.get('picture', '')
                user.given_name = payload.get('given_name', '')
                user.name = payload.get('name', '')
                user.email = payload.get('email', '')
                user.save()

                role = payload.get('http://localhost:4200/roles')[0]
                if role == 'student':
                    student_data = {
                        'user': user,
                        'grade': 4
                    }
                    student = Student(**student_data)
                    student.save()

                elif role == 'teacher':
                    teacher_data = {
                        'user': user,
                        'subject': 'Math'
                    }
                    teacher = Teacher(**teacher_data)
                    teacher.save()

            request.user = user
        else:
            request.user = AnonymousUser()

        return self.get_response(request)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def department_list(request):
    if request.method == 'GET':
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def teacher_list(request):
    if request.method == 'GET':
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def student_list(request):
    if request.method == 'GET':
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def course_list(request):
    if request.method == 'GET':
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only allow users to see their own enrollments
        return Enrollment.objects.filter(student__user=self.request.user)

    def perform_create(self, serializer):
        # Ensure the enrollment is for the current user
        serializer.save(student=self.request.user.student)


class AssignmentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only allow users to see their own assignments
        return Assignment.objects.filter(student__user=self.request.user)

    @action(detail=False, url_path='course/(?P<course_id>\d+)', methods=['get'])
    def course_assignments(self, request, course_id=None):
        assignments = self.get_queryset().filter(course__id=course_id)
        serializer = self.get_serializer(assignments, many=True)
        return Response(serializer.data)
