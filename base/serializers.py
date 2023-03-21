from rest_framework.serializers import ModelSerializer

from base.models import Teacher, Group, Student


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class TeacherSerializer(ModelSerializer):
    group = GroupSerializer(many=True)

    class Meta:
        model = Teacher
        fields = '__all__'


class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'