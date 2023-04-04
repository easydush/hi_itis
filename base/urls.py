from django.urls import path, include
from rest_framework import routers

from base.views import my_view, MyView, TeacherView, TeacherViewSet, CustomAuthToken, StudentViewSet, HomePageView, \
    stripe_config, create_checkout_session

router = routers.DefaultRouter()
router.register(r'teacher', TeacherViewSet)
router.register(r'students', StudentViewSet)

urlpatterns = [
    path('about/', my_view, name='my_view'),
    path('hello/', MyView.as_view()),
    path('home/', HomePageView.as_view()),
    path('teachers/', TeacherView.as_view()),
    path('', include(router.urls)),
    path('auth/', CustomAuthToken.as_view()),
    path('config/', stripe_config),
    path('create-checkout-session/', create_checkout_session),
]
