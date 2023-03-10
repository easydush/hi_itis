from django.urls import path, include
from rest_framework import routers

from base.views import my_view, MyView, TeacherView, TeacherViewSet, CustomAuthToken

router = routers.DefaultRouter()
router.register(r'teacher', TeacherViewSet)

urlpatterns = [
    path('about/', my_view, name='my_view'),
    path('hello/', MyView.as_view()),
    path('teachers/', TeacherView.as_view()),
    path('', include(router.urls)),
    path('api-token-auth/', CustomAuthToken.as_view())
]
