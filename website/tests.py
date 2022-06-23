
from django.test import TestCase
from website.models import Dbtest


class DbTestCase(TestCase):
    def setUp(self):
        Dbtest.objects.create(testfield1='testrest')

    def test_animals_can_speak(self):

        ob = Dbtest.objects.get(testfield1="testrest")
        self.assertEqual(ob.test(), 'testrest')
