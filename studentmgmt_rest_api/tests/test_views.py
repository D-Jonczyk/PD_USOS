from django.test import RequestFactory, TestCase
from rest_framework import status
from rest_framework.test import force_authenticate
from studentmgmt_rest_api.models import Course, Enrollment, Student, Teacher, Auth0User, Department
from studentmgmt_rest_api.views import enroll_in_course, get_student_courses, get_students_in_course, \
    get_teacher_courses, update_student_grade, department_list, student_list
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient


class ViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_enroll_in_course(self):
        # Create a test user, student, and course
        user = Auth0User.objects.create(nickname='testuser')
        student = Student.objects.create(user=user)
        course = Course.objects.create()

        # Check if an enrollment already exists for the student and course
        enrollment = Enrollment.objects.filter(student=student, course=course).first()

        # Prepare the request
        data = {'course_id': course.id}
        request = self.factory.post(reverse('enroll'), data)

        # Authenticate the request with the user's token
        force_authenticate(request, user=user)

        if enrollment:
            # If an enrollment exists, update the grade
            data['grade'] = 2  # Include the grade value in the request data
            request = self.factory.patch(reverse('update-grade', args=[course.id, student.id]), data)

        # Call the view function
        response = enroll_in_course(request)

        # Assert the response
        if enrollment:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['detail'], 'Enrollment updated successfully.')
            enrollment.refresh_from_db()
            self.assertEqual(enrollment.grade, 2)
        else:
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data['detail'], 'Enrollment successful.')
            self.assertEqual(student.enrollment_set.count(), 1)
            self.assertEqual(student.enrollment_set.first().course, course)
            self.assertEqual(student.enrollment_set.first().grade, None)  # Expecting None for grade

        # Check the grade if it was passed in the request
        if 'grade' in data:
            self.assertEqual(student.enrollment_set.first().grade, 2)

    def test_get_student_courses(self):
        # Create a test user and student
        user = Auth0User.objects.create(nickname='testuser')
        student = Student.objects.create(user=user)

        # Create some test courses
        course1 = Course.objects.create()
        course2 = Course.objects.create()

        # Enroll the student in the courses
        Enrollment.objects.create(student=student, course=course1)
        Enrollment.objects.create(student=student, course=course2)

        # Prepare the request
        request = self.factory.get(reverse('get-student-courses'))

        # Authenticate the request with the user's token
        force_authenticate(request, user=user)

        # Call the view function
        response = get_student_courses(request)

        # Assert the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['course_id'], course1.id)
        self.assertEqual(response.data[1]['course_id'], course2.id)

    def test_update_student_grade(self):
        # Create a test student and course
        student_user = Auth0User.objects.create(nickname='teststudent', auth0_id='student1')
        student = Student.objects.create(user=student_user)
        course = Course.objects.create()

        # Enroll the student in the course
        Enrollment.objects.create(student=student, course=course)

        # Prepare the request
        data = {'grade': 1}  # Set the grade to 'A'
        url = reverse('update-grade', args=[course.id, student.id])
        request = self.factory.put(url, data)

        # Authenticate the request with the student's token
        force_authenticate(request, user=student_user)

        # Call the view function
        response = update_student_grade(request, course_id=course.id, student_id=student.id)

        # Assert the response
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class EnrollmentTestCase(APITestCase):
    def setUp(self):
        self.student_user = Auth0User.objects.create(nickname='teststudent', auth0_id='student1')
        self.teacher_user = Auth0User.objects.create(nickname='testteacher', auth0_id='teacher1')
        self.student = Student.objects.create(user=self.student_user)
        self.teacher = Teacher.objects.create(user=self.teacher_user)

    def test_enroll_in_course_as_student(self):
        # Create a test course
        course = Course.objects.create()

        # Prepare the request data
        data = {'course_id': course.id}

        # Authenticate the request with the student's token
        self.client.force_authenticate(user=self.student_user)

        # Send a POST request to enroll in the course
        response = self.client.post(reverse('enroll'), data)

        # Assert the response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['detail'], 'Enrollment successful.')

        # Verify that the student is enrolled in the course
        enrollment = Enrollment.objects.get(student=self.student, course=course)
        self.assertIsNotNone(enrollment)

    def test_enroll_in_course_as_teacher(self):
        # Create a test course
        course = Course.objects.create()

        # Prepare the request data
        data = {'course_id': course.id}

        # Authenticate the request with the teacher's token
        self.client.force_authenticate(user=self.teacher_user)

        # Send a POST request to enroll in the course
        response = self.client.post(reverse('enroll'), data)

        # Assert the response
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserProfileViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a test user
        self.user = Auth0User.objects.create(nickname='testuser')

    def test_update_user_profile(self):
        url = reverse('profile')  # Adjust the URL if needed

        # Prepare the request data
        data = {
            'given_name': 'John',
            'name': 'Doe',
            'nickname': 'johndoe',
            'picture': 'https://example.com/avatar.jpg',
            'auth0_id': 'auth0id123',
        }

        # Authenticate the request with the user's token
        self.client.force_authenticate(user=self.user)

        # Send the PUT request
        response = self.client.put(url, data)

        # Assert the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['given_name'], data['given_name'])
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['nickname'], data['nickname'])
        self.assertEqual(response.data['picture'], data['picture'])
        self.assertEqual(response.data['auth0_id'], data['auth0_id'])

        # Refresh the user object from the database
        self.user.refresh_from_db()

        # Assert the updated user profile
        self.assertEqual(self.user.given_name, data['given_name'])
        self.assertEqual(self.user.name, data['name'])
        self.assertEqual(self.user.nickname, data['nickname'])
        self.assertEqual(self.user.picture, data['picture'])
        self.assertEqual(self.user.auth0_id, data['auth0_id'])

    def test_get_students_in_course(self):
        # Create a test teacher, course, and associated students
        teacher_user = Auth0User.objects.create(nickname='testteacher', auth0_id='teacher1')
        teacher = Teacher.objects.create(user=teacher_user)
        course = Course.objects.create(instructor=teacher)

        student1_user = Auth0User.objects.create(nickname='teststudent1', auth0_id='student1')
        student1 = Student.objects.create(user=student1_user)
        Enrollment.objects.create(student=student1, course=course)

        student2_user = Auth0User.objects.create(nickname='teststudent2', auth0_id='student2')
        student2 = Student.objects.create(user=student2_user)
        Enrollment.objects.create(student=student2, course=course)

        # Prepare the request
        url = reverse('get-students-in-course', args=[course.id])
        self.client.force_authenticate(user=teacher_user)
        response = self.client.get(url)

        # Assert the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
