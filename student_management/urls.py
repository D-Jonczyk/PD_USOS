from django.urls import path, include
from rest_framework import routers
from .views import CourseCreateView, DepartmentCreateView, \
    EnrollmentViewSet, AssignmentListCreateView, HelloView

router = routers.DefaultRouter()
# router.register('students', StudentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('courses', CourseCreateView.as_view(), name='course-create'),
    path('departments', DepartmentCreateView.as_view(), name='department-create'),
    # path('teachers', TeacherListView.as_view(), name='teachers'),
    # path('students', StudentViewSet.as_view({'get': 'list', 'post': 'create'}), name='student-list'),
    path('enrollments', EnrollmentViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='enrollments'),
    path('enrollments/<str:user_id>',  EnrollmentViewSet.as_view({'get': 'list'}), name='user-enrollments'),
    path('assignments', AssignmentListCreateView.as_view({'get': 'list', 'post': 'create'}), name='assignments'),
    # path('check_student', CheckStudentExistenceView.as_view(), name='check-student-existence'),
    path('hello', HelloView.as_view(), name='hello')
]