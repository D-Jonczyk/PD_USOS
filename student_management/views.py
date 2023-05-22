from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Student, Department, Teacher, Course, Enrollment, Assignment
from .serializers import StudentSerializer, CourseSerializer, DepartmentSerializer, \
    TeacherSerializer, EnrollmentSerializer, AssignmentSerializer


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


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


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


class TeacherListView(APIView):
    def get(self, request):
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckStudentExistenceView(APIView):
    def post(self, request):
        auth0_id = request.data.get('auth0_id')

        try:
            student = Student.objects.get(auth0_id=auth0_id)
            # Student exists, return success response
            return Response({'id': student.id}, status=200)
        except ObjectDoesNotExist:
            # Student does not exist, add student to the database
            student = request.data
            serializer = StudentSerializer(data=student)
            if serializer.is_valid():
                serializer.save()
            else:
                print(serializer.errors)
            # Return success response with serialized student data
            return Response(serializer.data, status=201)
