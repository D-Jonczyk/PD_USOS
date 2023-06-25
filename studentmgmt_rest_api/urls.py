from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import course_list, get_student_courses, enroll_in_course, UserProfileView, department_list, teacher_list, \
    public, private, admin_panel, get_teacher_courses, update_student_grade, get_students_in_course, \
    student_list, test_student, test_teacher


# /api prefix is added in pd_usos\urls.py
router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('courses', course_list),
    path('teacher/courses', get_teacher_courses),
    path('teacher/course/<int:course_id>/student/<int:student_id>/grade', update_student_grade),
    path('teacher/course/<int:course_id>/students', get_students_in_course),
    path('student-courses', get_student_courses),
    path('enroll', enroll_in_course),
    path('profile', UserProfileView.as_view(), name='profile'),
    path('departments', department_list),
    path('students', student_list),
    path('public', public),
    path('private', private),
    path('admin_panel', admin_panel),
    path('test_teacher', test_teacher),
    path('test_student', test_student)
]
