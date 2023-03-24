from django.urls import path, include
from rest_framework import routers

from base.views import my_view, MyView, TeacherView, TeacherViewSet, CustomAuthToken, StudentViewSet

router = routers.DefaultRouter()
router.register(r'teacher', TeacherViewSet)
router.register(r'students', StudentViewSet)

urlpatterns = [
    path('about/', my_view, name='my_view'),
    path('hello/', MyView.as_view()),
    path('teachers/', TeacherView.as_view()),
    path('', include(router.urls)),
    path('auth/', CustomAuthToken.as_view())
]
