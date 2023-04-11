from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.


class SubjectChoices(models.TextChoices):
    INF = 'INF', _('Informatics')
    ENG = 'ENG', _('English')
    PHYS = 'PHYS', _('Physics')


class Group(models.Model):
    title = models.CharField(max_length=40)
    course = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.title


class Student(models.Model):
    name = models.CharField(max_length=40)
    surname = models.CharField(max_length=40)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.group.title}: {self.surname} {self.name}'


class Teacher(models.Model):
    group = models.ManyToManyField(Group, related_name='teachers')
    name = models.CharField(max_length=40)
    surname = models.CharField(max_length=40)


class TeacherProfile(models.Model):
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE)
    key = models.SlugField()
    subject = models.CharField(max_length=20, choices=SubjectChoices.choices, default=SubjectChoices.INF)
