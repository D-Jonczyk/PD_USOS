from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import course_list, get_student_courses, enroll_in_course, UserProfileView, department_list, teacher_list, \
    get_teacher_courses, update_student_grade, get_students_in_course, \
    student_list


# /api prefix is added in pd_usos\urls.py
router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('courses', course_list),
    path('teacher/courses', get_teacher_courses),
    path('teacher/course/<int:course_id>/student/<int:student_id>/grade', update_student_grade, name='update-grade'),
    path('teacher/course/<int:course_id>/students', get_students_in_course, name='get-students-in-course'),
    path('student-courses', get_student_courses, name='get-student-courses'),
    path('enroll', enroll_in_course, name='enroll'),
    path('profile', UserProfileView.as_view(), name='profile'),
    path('departments', department_list, name='department-list'),
    path('students', student_list),
]
