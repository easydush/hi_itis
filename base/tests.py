from django.test import TestCase

from base.models import Student, Group

class StudentTestCase(TestCase):
    def setUp(self):
        self.group = Group.objects.create(title='11-105', course=2)
        self.student = Student.objects.create(name="Jordan", group_id=self.group.id, surname='Baker')

    def test_student_str(self):
        self.assertEqual(str(self.student), f'{self.group.title}: {self.student.surname} {self.student.name}')
        """Animals that can speak are correctly identified"""
        # lion = Animal.objects.get(name="lion")
        # cat = Animal.objects.get(name="cat")
        # self.assertEqual(lion.speak(), 'The lion says "roar"')
        # self.assertEqual(cat.speak(), 'The cat says "meow"')