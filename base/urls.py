from django.urls import path

from base.views import my_view, MyView, TeacherView

urlpatterns = [
    path('about/', my_view, name='my_view'),
    path('hello/', MyView.as_view()),
    path('teachers/', TeacherView.as_view()),
]
