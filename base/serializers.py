from rest_framework.serializers import ModelSerializer

from base.models import Teacher, Group


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class TeacherSerializer(ModelSerializer):
    group = GroupSerializer(many=True)

    class Meta:
        model = Teacher
        fields = '__all__'
