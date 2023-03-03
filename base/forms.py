from django.forms import ModelForm

from base.models import Student, Teacher


class MyForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'


class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'
