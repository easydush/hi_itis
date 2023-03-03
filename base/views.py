from django.shortcuts import render, redirect

# Create your views here
from django.http import HttpResponse
from django.views import View
from rest_framework import viewsets

from base.forms import MyForm, TeacherForm
from base.models import Student, Teacher
from base.serializers import TeacherSerializer


def my_view(request):
    print(request.method, request.path)
    if request.method == 'GET':
        student = Student.objects.all()
        respones_data = '; '.join(', '.join(value) for value in student.values_list('name', 'surname', 'group__title'))
        return HttpResponse(respones_data)


class MyView(View):
    def get(self, request):
        students = Student.objects.all()

        form = MyForm()

        context = {'students': students, 'form': form}

        return render(request, 'hello.html', context=context)

    def post(self, request):
        print(request.POST)
        form = MyForm(request.POST)
        if form.is_valid():
            student = Student.objects.create(**form.cleaned_data)
            return redirect('/hello')


class TeacherView(View):
    def get(self, request):
        teachers = Teacher.objects.all()

        form = TeacherForm()

        context = {'teachers': teachers, 'form': form}

        return render(request, 'teachers.html', context=context)

    def post(self, request):
        print(request.POST)
        form = TeacherForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            teacher = form.save(commit=False)
            teacher.save()
            form.save_m2m()

            return redirect('/teachers')


# ViewSets define the view behavior.
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
