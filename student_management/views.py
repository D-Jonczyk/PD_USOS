from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import viewsets, generics, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Student, Department, Teacher, Course, Enrollment, Assignment
from .serializers import StudentSerializer, CourseSerializer, DepartmentSerializer, \
    TeacherSerializer, EnrollmentSerializer, AssignmentSerializer
import requests


class HelloView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            user_info = {
                'username': user.nickname,
                'email': user.email,
                'first_name': user.given_name,
                'last_name': user.name
                # Add more user information fields as needed
            }
            content = {'message': 'Hello, Authenticated User!', 'user': user_info}
            return Response(content)
        else:
            return Response({'message': 'You must be authenticated to access this endpoint.'}, status=403)


class Auth0Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(' ')[1]  # Assuming Bearer token
            userinfo_endpoint = 'https://dev-gybtlqrqithbjmgz.us.auth0.com/userinfo'
            headers = {'Authorization': f'Bearer {token}'}

            response = requests.get(userinfo_endpoint, headers=headers)
            if response.status_code == 200:
                user_info = response.json()
                print("user info in middleware", user_info)

                User = get_user_model()
                user_id = user_info['sub']
                user, created = User.objects.get_or_create(auth0_id=user_id)
                if created:
                    user.nickname = user_info.get('nickname', '')
                    user.picture = user_info.get('picture', '')
                    user.given_name = user_info.get('given_name', '')
                    user.family_name = user_info.get('family_name', '')
                    user.name = user_info.get('name', '')
                    user.save()

                    role = user_info.get('http://localhost:4200/roles')[0]
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
                raise AuthenticationFailed('Invalid token')

        return self.get_response(request)


class DepartmentCreateView(APIView):
    def get(self, request):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data

        # Check if required fields are present
        if 'name' not in data or 'description' not in data:
            return Response(
                {'error': 'Required fields are missing'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Retrieve field values
        name = data['name']
        description = data['description']

        # Perform additional validation if needed
        if not name.strip() or not description.strip():
            return Response(
                {'error': 'Fields cannot be empty or contain only whitespace'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create the department
        department = Department.objects.create(name=name, description=description)

        # Serialize the created department if necessary
        serializer = DepartmentSerializer(department)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


# class StudentViewSet(viewsets.ModelViewSet):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer
#
#     def get_object(self):
#         queryset = self.get_queryset()
#         filter_kwargs = {'auth0_id': self.request.user.auth0_id}  # Modify the filter based on your authentication
#         # mechanism
#         obj = get_object_or_404(queryset, **filter_kwargs)
#         self.check_object_permissions(self.request, obj)
#         return obj
#

class EnrollmentViewSet(viewsets.ModelViewSet):
    def list(self, request, user_id=None):
        # Retrieve enrollments for the specified user_id
        enrollments = Enrollment.objects.filter(student_id=user_id)
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)

    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer


class AssignmentListCreateView(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer


class CourseCreateView(APIView):
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class TeacherListView(APIView):
#     def get(self, request):
#         teachers = Teacher.objects.all()
#         serializer = TeacherSerializer(teachers, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = TeacherSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CheckStudentExistenceView(APIView):
#     def post(self, request):
#         auth0_id = request.data.get('auth0_id')
#
#         try:
#             student = Student.objects.get(auth0_id=auth0_id)
#             # Student exists, return success response
#             return Response({'id': student.id}, status=200)
#         except ObjectDoesNotExist:
#             # Student does not exist, add student to the database
#             student = request.data
#             serializer = StudentSerializer(data=student)
#             if serializer.is_valid():
#                 serializer.save()
#             else:
#                 print(serializer.errors)
#             # Return success response with serialized student data
#             return Response(serializer.data, status=201)
