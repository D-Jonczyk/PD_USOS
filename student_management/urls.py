from django.urls import path, include
from rest_framework import routers
from .views import StudentViewSet

router = routers.DefaultRouter()
router.register('students', StudentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('students/', views.StudentList.as_view(), name='student-list'),
]
