from django.test import TestCase
from django.contrib.auth import get_user_model
from recognizer.models import TrainingGroup


class TestTrainingGroup(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test_email@example.com', 
            name='test_user',
            password='test_password',
        )
        self.group = TrainingGroup.objects.create(name='test_group', owner=self.user)

    def test_owner(self):
        self.assertEqual(self.group.owner, self.user)

    def test_update(self):
        self.group.name = 'updated_group'
        self.group.save()
        self.assertEqual(self.group.name, 'updated_group')

    def test_delete(self):
        self.assertEqual(TrainingGroup.objects.count(), 1)
        self.group.delete()
        self.assertEqual(TrainingGroup.objects.count(), 0)
